import requests
import os
from PIL import Image
import numpy as np

# Configuration
API_URL = "http://localhost:8000"
SAMPLE_IMAGE_PATH = "test_xray.png"
PATIENT_ID = "TEST_PATIENT_001"


def create_sample_xray():
    """Create a sample grayscale image for testing"""
    if not os.path.exists(SAMPLE_IMAGE_PATH):
        print("📸 Creating sample X-ray image...")
        # Create a simple grayscale image
        img_array = np.random.randint(50, 200, (512, 512), dtype=np.uint8)
        img = Image.fromarray(img_array, mode='L')
        img.save(SAMPLE_IMAGE_PATH)
        print(f"✓ Sample image created: {SAMPLE_IMAGE_PATH}")
    else:
        print(f"ℹ Using existing image: {SAMPLE_IMAGE_PATH}")


def test_health():
    """Test health check endpoint"""
    print("\n" + "=" * 50)
    print("Testing Health Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_predict():
    """Test prediction endpoint"""
    print("\n" + "=" * 50)
    print("Testing Prediction Endpoint")
    print("=" * 50)
    
    try:
        with open(SAMPLE_IMAGE_PATH, 'rb') as f:
            files = {'image': ('test_xray.png', f, 'image/png')}
            data = {'patient_id': PATIENT_ID}
            
            print(f"📤 Uploading image for patient: {PATIENT_ID}")
            response = requests.post(f"{API_URL}/predict", files=files, data=data)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("\n✓ Prediction Successful!")
                print(f"\nPatient ID: {result['patient_id']}")
                print(f"Prediction ID: {result['prediction_id']}")
                print(f"MLflow Run ID: {result['mlflow_run_id']}")
                
                print("\n📊 Male Model Results:")
                male = result['male_prediction']
                print(f"  Age: {male['age']} years")
                print(f"  Uncertainty (σ): {male['uncertainty_sigma']}")
                print(f"  Grad-CAM: {male['gradcam_url']}")
                
                print("\n📊 Female Model Results:")
                female = result['female_prediction']
                print(f"  Age: {female['age']} years")
                print(f"  Uncertainty (σ): {female['uncertainty_sigma']}")
                print(f"  Grad-CAM: {female['gradcam_url']}")
                
                return True
            else:
                print(f"✗ Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_get_results():
    """Test get results endpoint"""
    print("\n" + "=" * 50)
    print("Testing Get Results Endpoint")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_URL}/results/{PATIENT_ID}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n✓ Results Retrieved!")
            print(f"Patient ID: {result['patient_id']}")
            print(f"Total Predictions: {result['total_predictions']}")
            
            for i, pred in enumerate(result['predictions'], 1):
                print(f"\nPrediction {i}:")
                print(f"  Timestamp: {pred['timestamp']}")
                print(f"  Male Age: {pred['male_age']} (σ={pred['male_uncertainty']})")
                print(f"  Female Age: {pred['female_age']} (σ={pred['female_uncertainty']})")
            
            return True
        else:
            print(f"✗ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Bone Age Estimation API Test Suite")
    print("=" * 50)
    
    # Create sample image
    create_sample_xray()
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Prediction": test_predict(),
        "Get Results": test_get_results()
    }
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠ Some tests failed. Check the API server.")


if __name__ == "__main__":
    main()
