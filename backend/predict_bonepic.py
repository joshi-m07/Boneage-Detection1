import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
IMAGE_PATH = "Bonepic.jpg"
PATIENT_ID = f"REAL_PATIENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

print("=" * 60)
print("🦴 BONE AGE ESTIMATION - Real X-ray Analysis")
print("=" * 60)
print(f"\n📸 Image: {IMAGE_PATH}")
print(f"👤 Patient ID: {PATIENT_ID}")
print("\n🔄 Sending prediction request...")

try:
    # Send prediction request
    with open(IMAGE_PATH, 'rb') as f:
        files = {'image': (IMAGE_PATH, f, 'image/jpeg')}
        data = {'patient_id': PATIENT_ID}
        
        response = requests.post(f"{API_URL}/predict", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n" + "=" * 60)
        print("✅ PREDICTION SUCCESSFUL!")
        print("=" * 60)
        
        print(f"\n📋 Patient ID: {result['patient_id']}")
        print(f"🔢 Prediction ID: {result['prediction_id']}")
        print(f"📊 MLflow Run ID: {result['mlflow_run_id']}")
        
        print("\n" + "-" * 60)
        print("👨 MALE MODEL PREDICTION")
        print("-" * 60)
        male = result['male_prediction']
        print(f"  🎯 Predicted Age: {male['age']} ± {male['uncertainty_sigma']} years")
        print(f"  🔥 Grad-CAM Heatmap: {male['gradcam_path']}")
        
        print("\n" + "-" * 60)
        print("👩 FEMALE MODEL PREDICTION")
        print("-" * 60)
        female = result['female_prediction']
        print(f"  🎯 Predicted Age: {female['age']} ± {female['uncertainty_sigma']} years")
        print(f"  🔥 Grad-CAM Heatmap: {female['gradcam_path']}")
        
        print("\n" + "=" * 60)
        print("📁 RESULTS SAVED TO:")
        print("=" * 60)
        print(f"  💾 Database: boneage_predictions.db")
        print(f"  📂 Images: data/storage/patients/{result['patient_id']}/")
        print(f"     • original.png")
        print(f"     • male_gradcam.png")
        print(f"     • female_gradcam.png")
        print(f"  📊 MLflow: data/mlruns/ (view at http://localhost:5000)")
        
        print("\n" + "=" * 60)
        print("🎉 PROCESS COMPLETE!")
        print("=" * 60)
        
        # Pretty print full JSON response
        print("\n📄 Full JSON Response:")
        print(json.dumps(result, indent=2))
        
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except FileNotFoundError:
    print(f"\n❌ Error: Could not find image file '{IMAGE_PATH}'")
    print("Please make sure Bonepic.jpeg is in the current directory.")
except Exception as e:
    print(f"\n❌ Error: {e}")
