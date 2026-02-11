import requests
import json

# Get the latest results
patient_id = "REAL_PATIENT_20260203_195736"

print("=" * 70)
print("🦴 BONE AGE ESTIMATION RESULTS - Bonepic.jpg")
print("=" * 70)

response = requests.get(f"http://localhost:8000/results/{patient_id}")

if response.status_code == 200:
    data = response.json()
    
    print(f"\n👤 Patient ID: {data['patient_id']}")
    print(f"📅 Upload Time: {data['upload_timestamp']}")
    print(f"📊 Total Predictions: {data['total_predictions']}")
    
    for i, pred in enumerate(data['predictions'], 1):
        print(f"\n{'━' * 70}")
        print(f"PREDICTION #{i}")
        print('━' * 70)
        print(f"🕐 Timestamp: {pred['timestamp']}")
        print(f"🔢 Prediction ID: {pred['prediction_id']}")
        print(f"📊 MLflow Run ID: {pred['mlflow_run_id']}")
        
        print(f"\n👨 MALE MODEL:")
        print(f"   🎯 Age: {pred['male_age']} years")
        print(f"   📉 Uncertainty (σ): {pred['male_uncertainty']}")
        
        print(f"\n👩 FEMALE MODEL:")
        print(f"   🎯 Age: {pred['female_age']} years")
        print(f"   📉 Uncertainty (σ): {pred['female_uncertainty']}")
    
    print(f"\n{'=' * 70}")
    print("📁 GENERATED FILES")
    print('=' * 70)
    print(f"📂 Location: storage/patients/{patient_id}/")
    print(f"   ✅ original.png - Your uploaded X-ray")
    print(f"   ✅ male_gradcam.png - Male model heatmap visualization")
    print(f"   ✅ female_gradcam.png - Female model heatmap visualization")
    
    print(f"\n{'=' * 70}")
    print("💾 DATA STORED IN")
    print('=' * 70)
    print(f"   ✅ SQLite Database: boneage_predictions.db")
    print(f"   ✅ MLflow Tracking: mlruns/ (view at http://localhost:5000)")
    
    print(f"\n{'=' * 70}")
    print("✅ PROCESS COMPLETED SUCCESSFULLY!")
    print('=' * 70)
    
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
