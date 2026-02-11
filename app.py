from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from PIL import Image
import io
import os
import shutil
from datetime import datetime

from database.db import get_db, init_db
from database.models import Patient, Prediction
from utils.inference import get_inference_model
from utils.gradcam_utils import GradCAMGenerator
from mlflow_config import mlflow_config

# Initialize FastAPI app
app = FastAPI(
    title="Bone Age Estimation API",
    description="Real-time bone age estimation using dual models with MLflow tracking",
    version="1.0.0"
)

# Storage directory
STORAGE_DIR = "storage/patients"
os.makedirs(STORAGE_DIR, exist_ok=True)


def normalize_path_for_storage(path):
    """
    Normalize path for cross-platform storage in database.
    Converts backslashes to forward slashes for compatibility.
    
    Args:
        path: File path string
    
    Returns:
        str: Normalized path with forward slashes
    """
    return path.replace("\\", "/")


@app.on_event("startup")
async def startup_event():
    """Initialize database and models on startup"""
    print("=" * 50)
    print("🚀 Starting Bone Age Estimation API")
    print("=" * 50)
    init_db()
    # Preload models
    get_inference_model()
    print("=" * 50)
    print("✅ API Ready!")
    print("=" * 50)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Bone Age Estimation API is running",
        "version": "1.0.0"
    }


@app.post("/predict")
async def predict_bone_age(
    image: UploadFile = File(..., description="X-ray image file"),
    patient_id: str = Form(..., description="Patient ID for tracking"),
    db: Session = Depends(get_db)
):
    """
    Main prediction endpoint following the pipeline:
    1. Image Upload & Validation
    2. Store Image (patient-wise for traceability)
    3. Start MLflow Run (gender = unknown)
    4. On-the-fly Augmentation
    5. Preprocessing
    6. Male Model Inference (age, uncertainty, Grad-CAM)
    7. Female Model Inference (age, uncertainty, Grad-CAM)
    8. MLflow Logging (both predictions)
    9. Store Results in Database
    10. Return Dual Prediction
    """
    
    try:
        # ===== STEP 1: Validation =====
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Validate it's an X-ray (grayscale or can be converted)
        pil_image = pil_image.convert('L')
        
        # ===== STEP 2: Store Image =====
        patient_dir = os.path.join(STORAGE_DIR, patient_id)
        os.makedirs(patient_dir, exist_ok=True)
        
        original_image_path = os.path.join(patient_dir, "original.png")
        pil_image.save(original_image_path)
        
        # Check if patient exists in database
        db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
        if not db_patient:
            db_patient = Patient(
                patient_id=patient_id,
                image_path=normalize_path_for_storage(original_image_path)
            )
            db.add(db_patient)
            db.commit()
            db.refresh(db_patient)
        
        # ===== STEP 3: Start MLflow Run =====
        run = mlflow_config.start_run(run_name=f"patient_{patient_id}")
        run_id = mlflow_config.get_run_id()
        
        # Log parameters
        mlflow_config.log_params({
            "patient_id": patient_id,
            "gender": "unknown",  # As per pipeline diagram
            "image_size": f"{pil_image.size[0]}x{pil_image.size[1]}",
            "timestamp": datetime.now().isoformat()
        })
        
        # ===== STEP 4-6: Male Model Inference =====
        inference_model = get_inference_model()
        
        # Male prediction
        male_result = inference_model.infer_male(pil_image)
        male_age = male_result['age']
        male_uncertainty = male_result['uncertainty']
        
        # Generate Male Grad-CAM
        male_heatmap = inference_model.generate_gradcam(
            male_result['input_tensor'],
            male_result['original_image'],
            model_type='male'
        )
        male_gradcam_path = os.path.join(patient_dir, "male_gradcam.png")
        male_gradcam_path_normalized = normalize_path_for_storage(male_gradcam_path)
        inference_model.male_gradcam.save_visualization(
            pil_image,
            male_heatmap,
            male_gradcam_path
        )
        
        # ===== STEP 7: Female Model Inference =====
        female_result = inference_model.infer_female(pil_image)
        female_age = female_result['age']
        female_uncertainty = female_result['uncertainty']
        
        # Generate Female Grad-CAM
        female_heatmap = inference_model.generate_gradcam(
            female_result['input_tensor'],
            female_result['original_image'],
            model_type='female'
        )
        female_gradcam_path = os.path.join(patient_dir, "female_gradcam.png")
        female_gradcam_path_normalized = normalize_path_for_storage(female_gradcam_path)
        inference_model.female_gradcam.save_visualization(
            pil_image,
            female_heatmap,
            female_gradcam_path
        )
        
        # ===== STEP 8: MLflow Logging =====
        mlflow_config.log_metrics({
            "male_age": male_age,
            "male_uncertainty": male_uncertainty,
            "female_age": female_age,
            "female_uncertainty": female_uncertainty,
        })
        
        # Log artifacts
        mlflow_config.log_artifact(original_image_path)
        mlflow_config.log_artifact(male_gradcam_path)
        mlflow_config.log_artifact(female_gradcam_path)
        
        # End MLflow run
        mlflow_config.end_run()
        
        # ===== STEP 9: Store Results in Database =====
        db_prediction = Prediction(
            patient_id=db_patient.id,
            male_age=male_age,
            male_uncertainty=male_uncertainty,
            male_gradcam_path=male_gradcam_path_normalized,
            female_age=female_age,
            female_uncertainty=female_uncertainty,
            female_gradcam_path=female_gradcam_path_normalized,
            mlflow_run_id=run_id
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        
        # ===== STEP 10: Return Dual Prediction =====
        # Use relative paths for portability across different machines
        male_gradcam_relative = os.path.relpath(male_gradcam_path)
        female_gradcam_relative = os.path.relpath(female_gradcam_path)
        
        response = {
            "status": "success",
            "patient_id": patient_id,
            "prediction_id": db_prediction.id,
            "mlflow_run_id": run_id,
            "male_prediction": {
                "age": round(male_age, 2),
                "uncertainty_sigma": round(male_uncertainty, 3),
                "gradcam_path": male_gradcam_relative,
                "gradcam_url": f"/storage/{patient_id}/male_gradcam.png"
            },
            "female_prediction": {
                "age": round(female_age, 2),
                "uncertainty_sigma": round(female_uncertainty, 3),
                "gradcam_path": female_gradcam_relative,
                "gradcam_url": f"/storage/{patient_id}/female_gradcam.png"
            },
            "timestamp": datetime.now().isoformat(),
            "message": "Male & Female Bone Age Results"
        }
        
        return JSONResponse(content=response, status_code=200)
    
    except Exception as e:
        # Ensure MLflow run is ended even on error
        if mlflow_config.get_run_id():
            mlflow_config.end_run()
        
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/results/{patient_id}")
async def get_patient_results(patient_id: str, db: Session = Depends(get_db)):
    """
    Retrieve stored prediction results for a patient
    
    Args:
        patient_id: Patient ID
    
    Returns:
        Patient information and all predictions
    """
    # Get patient
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get all predictions for this patient
    predictions = db_patient.predictions
    
    results = {
        "patient_id": patient_id,
        "upload_timestamp": db_patient.upload_timestamp.isoformat(),
        "total_predictions": len(predictions),
        "predictions": []
    }
    
    for pred in predictions:
        results["predictions"].append({
            "prediction_id": pred.id,
            "timestamp": pred.prediction_timestamp.isoformat(),
            "male_age": round(pred.male_age, 2),
            "male_uncertainty": round(pred.male_uncertainty, 3),
            "female_age": round(pred.female_age, 2),
            "female_uncertainty": round(pred.female_uncertainty, 3),
            "mlflow_run_id": pred.mlflow_run_id
        })
    
    return results


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "models": "loaded",
        "database": "connected",
        "mlflow": "initialized"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
