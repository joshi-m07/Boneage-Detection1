# Bone Age Estimation Backend

Real-time bone age estimation pipeline using dual models (male/female) with MLflow tracking, Grad-CAM visualization, and uncertainty estimation.

## 🏗️ Architecture

The backend follows the pipeline:
1. **Image Upload** - Accept X-ray images
2. **Validation** - Verify image format
3. **Storage** - Patient-wise image storage for traceability
4. **MLflow Run** - Start experiment tracking (gender=unknown)
5. **Augmentation** - On-the-fly image augmentation
6. **Preprocessing** - Normalize and resize images
7. **Male Model Inference** - Predict age, uncertainty (σ), and generate Grad-CAM
8. **Female Model Inference** - Predict age, uncertainty (σ), and generate Grad-CAM
9. **MLflow Logging** - Log both predictions and artifacts
10. **Database Storage** - Store results for later retrieval
11. **Return Response** - Dual predictions with male & female results

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Start the API server
python app.py

# Or use uvicorn directly
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### 1. Predict Bone Age
**POST** `/predict`

Upload an X-ray image and get bone age predictions from both models.

**Request:**
- `image` (file): X-ray image file
- `patient_id` (string): Patient identifier

**Response:**
```json
{
  "status": "success",
  "patient_id": "PATIENT001",
  "prediction_id": 1,
  "mlflow_run_id": "abc123...",
  "male_prediction": {
    "age": 12.5,
    "uncertainty_sigma": 0.234,
    "gradcam_path": "storage/patients/PATIENT001/male_gradcam.png",
    "gradcam_url": "/storage/PATIENT001/male_gradcam.png"
  },
  "female_prediction": {
    "age": 11.8,
    "uncertainty_sigma": 0.198,
    "gradcam_path": "storage/patients/PATIENT001/female_gradcam.png",
    "gradcam_url": "/storage/PATIENT001/female_gradcam.png"
  },
  "timestamp": "2026-02-03T19:30:00",
  "message": "Male & Female Bone Age Results"
}
```

### 2. Get Patient Results
**GET** `/results/{patient_id}`

Retrieve all predictions for a specific patient.

### 3. Health Check
**GET** `/health`

Check API health status.

## 🔬 MLflow Tracking

View experiment logs and artifacts:

```bash
# Start MLflow UI
mlflow ui

# Open browser to http://localhost:5000
```

MLflow logs:
- **Parameters**: patient_id, gender (unknown), image_size, timestamp
- **Metrics**: male_age, male_uncertainty, female_age, female_uncertainty
- **Artifacts**: original image, male Grad-CAM, female Grad-CAM

## 📊 Database

SQLite database stores:
- **Patients**: patient_id, image_path, upload_timestamp
- **Predictions**: male/female ages, uncertainties, Grad-CAM paths, MLflow run ID

Database file: `boneage_predictions.db`

## 📁 Directory Structure

```
Boneage Detection/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── mlflow_config.py           # MLflow configuration
├── database/
│   ├── __init__.py
│   ├── db.py                  # Database connection
│   └── models.py              # SQLAlchemy models
├── utils/
│   ├── __init__.py
│   ├── inference.py           # Model loading & inference
│   ├── gradcam_utils.py       # Grad-CAM generation
│   └── augmentation.py        # Image augmentation
├── male_boneage/
│   └── male_boneage/
│       ├── model.py           # Model architecture
│       └── gradcam.py         # Grad-CAM implementation
├── male_boneage_model.pth     # Male model weights
├── female_boneage_model.pth   # Female model weights (optional)
├── storage/
│   └── patients/
│       └── {patient_id}/
│           ├── original.png
│           ├── male_gradcam.png
│           └── female_gradcam.png
└── mlruns/                    # MLflow tracking data
```

## 🧪 Testing

Use the provided test script:

```bash
python test_api.py
```

Or use curl:

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "image=@sample_xray.png" \
  -F "patient_id=TEST001"
```

## ⚠️ Important Notes

1. **Female Model**: If `female_boneage_model.pth` is not present, the system will use the male model for both predictions. Train and add the female model for accurate dual predictions.

2. **Model Outputs**: 
   - `grp` output: 4-class age group classification (0-5, 5-10, 10-15, 15-20 years)
   - `unc` output: 2-dimensional uncertainty estimation
   - Returns midpoint of predicted age group and uncertainty σ

3. **Storage**: Patient images and Grad-CAMs are stored in `storage/patients/{patient_id}/` for traceability.

4. **MLflow**: All predictions are logged to MLflow with `gender=unknown` as specified in the pipeline.

## 🔧 Configuration

Edit `mlflow_config.py` to change:
- Experiment name
- Tracking URI (for remote MLflow server)

Edit `database/db.py` to change:
- Database type (PostgreSQL, MySQL, etc.)
- Connection settings

## 📝 API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

**CUDA out of memory:**
```python
# In utils/inference.py, change device to 'cpu'
_inference_instance = ModelInference(male_model_path, female_model_path, device='cpu')
```

**Database errors:**
```bash
# Delete and reinitialize database
rm boneage_predictions.db
python -c "from database.db import init_db; init_db()"
```

**MLflow errors:**
```bash
# Clear MLflow runs
rm -rf mlruns/
```
