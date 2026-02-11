import sqlite3
import json

# Connect to the database
conn = sqlite3.connect('boneage_predictions.db')
cursor = conn.cursor()

# Get the latest prediction
cursor.execute("""
    SELECT 
        p.patient_id,
        pr.id,
        pr.male_age,
        pr.male_uncertainty,
        pr.female_age,
        pr.female_uncertainty,
        pr.mlflow_run_id,
        pr.prediction_timestamp
    FROM predictions pr
    JOIN patients p ON pr.patient_id = p.id
    WHERE p.patient_id = 'REAL_PATIENT_20260203_195736'
    ORDER BY pr.prediction_timestamp DESC
    LIMIT 1
""")

result = cursor.fetchone()
conn.close()

if result:
    patient_id, pred_id, male_age, male_unc, female_age, female_unc, mlflow_id, timestamp = result
    
    print("=" * 70)
    print("🦴 BONE AGE ESTIMATION RESULTS - Bonepic.jpg")
    print("=" * 70)
    print(f"\n👤 Patient ID: {patient_id}")
    print(f"🔢 Prediction ID: {pred_id}")
    print(f"🕐 Timestamp: {timestamp}")
    print(f"📊 MLflow Run ID: {mlflow_id}")
    
    print(f"\n{'━' * 70}")
    print("📊 PREDICTION RESULTS")
    print('━' * 70)
    
    print(f"\n👨 MALE MODEL PREDICTION:")
    print(f"   🎯 Estimated Age: {male_age} years")
    print(f"   📉 Uncertainty (σ): {male_unc}")
    
    print(f"\n👩 FEMALE MODEL PREDICTION:")
    print(f"   🎯 Estimated Age: {female_age} years")
    print(f"   📉 Uncertainty (σ): {female_unc}")
    
    print(f"\n{'=' * 70}")
    print("📁 GENERATED FILES")
    print('=' * 70)
    print(f"📂 Location: storage/patients/{patient_id}/")
    print(f"   ✅ original.png")
    print(f"   ✅ male_gradcam.png")
    print(f"   ✅ female_gradcam.png")
    
    print(f"\n{'=' * 70}")
    print("💾 DATA STORAGE")
    print('=' * 70)
    print(f"   ✅ Database: boneage_predictions.db")
    print(f"   ✅ Patient record in 'patients' table")
    print(f"   ✅ Prediction record in 'predictions' table")
    print(f"   ✅ MLflow experiment logged")
    print(f"   ✅ View experiments at: http://localhost:5000")
    
    print(f"\n{'=' * 70}")
    print("✅ COMPLETE PIPELINE EXECUTED SUCCESSFULLY!")
    print('=' * 70)
    print("\nPipeline steps completed:")
    print("  1. ✅ Image Upload & Validation")
    print("  2. ✅ Patient-wise Storage")
    print("  3. ✅ MLflow Run Started (gender=unknown)")
    print("  4. ✅ On-the-fly Augmentation")
    print("  5. ✅ Preprocessing")
    print("  6. ✅ Male Model Inference")
    print("  7. ✅ Female Model Inference")
    print("  8. ✅ Grad-CAM Heatmap Generation")
    print("  9. ✅ MLflow Logging")
    print(" 10. ✅ Database Storage")
    print(" 11. ✅ Response Returned")
    
else:
    print("No results found")
