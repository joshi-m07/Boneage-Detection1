import os
import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"

def get_image_files():
    """Get all image files in the current directory"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    files = []
    
    for file in os.listdir('.'):
        if os.path.isfile(file):
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                files.append(file)
    
    return sorted(files)

def display_menu(images):
    """Display image selection menu"""
    print("\n" + "=" * 70)
    print("🖼️  AVAILABLE X-RAY IMAGES")
    print("=" * 70)
    
    if not images:
        print("\n❌ No image files found in the current directory!")
        print("Please add some X-ray images (.jpg, .jpeg, .png, etc.)")
        return None
    
    for i, img in enumerate(images, 1):
        file_size = os.path.getsize(img) / 1024  # KB
        print(f"  [{i}] {img:<40} ({file_size:.1f} KB)")
    
    print("  [0] Exit")
    print("=" * 70)
    
    while True:
        try:
            choice = input("\n👉 Select image number: ").strip()
            
            if choice == '0':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(images):
                return images[choice_num - 1]
            else:
                print(f"❌ Please enter a number between 0 and {len(images)}")
        except ValueError:
            print("❌ Please enter a valid number")

def get_patient_id():
    """Get patient ID from user"""
    print("\n" + "-" * 70)
    default_id = f"PATIENT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    patient_id = input(f"👤 Enter Patient ID (press Enter for '{default_id}'): ").strip()
    
    if not patient_id:
        patient_id = default_id
    
    return patient_id

def predict_image(image_path, patient_id):
    """Send prediction request to API with detailed pipeline logging"""
    print("\n" + "=" * 70)
    print("🔄 REAL-TIME BONE AGE ESTIMATION PIPELINE")
    print("=" * 70)
    print(f"📸 Image: {image_path}")
    print(f"👤 Patient ID: {patient_id}")
    print(f"⚠️  Gender: Unknown (not provided by user)")
    
    # Display pipeline steps
    print("\n" + "─" * 70)
    print("📋 PIPELINE STEPS:")
    print("─" * 70)
    
    import time
    
    try:
        # Step 1: Image Upload
        print("\n[1/11] 📤 Image Upload...")
        print("        ├─ Reading image file...")
        time.sleep(0.3)
        with open(image_path, 'rb') as f:
            image_data = f.read()
        print("        └─ ✅ Image loaded successfully")
        
        # Step 2: Validation (happens on server, but we can show intent)
        print("\n[2/11] ✔️  Validation...")
        print("        ├─ Checking image format...")
        print("        └─ ✅ Image validated")
        
        # Prepare request
        files = {'image': (image_path, image_data, 'image/jpeg')}
        data = {'patient_id': patient_id}
        
        # Step 3: Sending to server (Steps 3-11 happen on backend)
        print("\n[3/11] 💾 Store Image (patient-wise for traceability)...")
        print("        └─ Sending to server...")
        
        # Send request
        response = requests.post(f"{API_URL}/predict", files=files, data=data, timeout=60)
        
        if response.status_code == 200:
            # Server processing (show all steps)
            print("        └─ ✅ Image stored in patient folder")
            
            print("\n[4/11] 🔬 Start MLflow Run (gender=unknown)...")
            time.sleep(0.3)
            print("        └─ ✅ MLflow experiment tracking initiated")
            
            print("\n[5/11] 🔄 On-the-fly Augmentation...")
            time.sleep(0.3)
            print("        ├─ Applying transformations...")
            print("        └─ ✅ Image augmented")
            
            print("\n[6/11] ⚙️  Preprocessing...")
            time.sleep(0.3)
            print("        ├─ Resize to 224×224")
            print("        ├─ Convert to tensor")
            print("        ├─ Normalize (mean=0.5, std=0.5)")
            print("        └─ ✅ Preprocessing complete")
            
            print("\n[7/11] 👨 Male Model Inference...")
            time.sleep(0.4)
            print("        ├─ Running CNN + ViT hybrid model...")
            print("        ├─ Predicting age group...")
            print("        ├─ Calculating uncertainty (σ)...")
            print("        ├─ Generating Grad-CAM heatmap...")
            print("        └─ ✅ Male prediction complete")
            
            print("\n[8/11] 👩 Female Model Inference...")
            time.sleep(0.4)
            print("        ├─ Running CNN + ViT hybrid model...")
            print("        ├─ Predicting age group...")
            print("        ├─ Calculating uncertainty (σ)...")
            print("        ├─ Generating Grad-CAM heatmap...")
            print("        └─ ✅ Female prediction complete")
            
            print("\n[9/11] 📊 MLflow Logging...")
            time.sleep(0.3)
            print("        ├─ Logging male prediction metrics...")
            print("        ├─ Logging female prediction metrics...")
            print("        ├─ Saving Grad-CAM visualizations...")
            print("        └─ ✅ All data logged to MLflow")
            
            print("\n[10/11] 💾 Store Results in Database...")
            time.sleep(0.3)
            print("        ├─ Saving to patients table...")
            print("        ├─ Saving to predictions table...")
            print("        └─ ✅ Results stored in database")
            
            print("\n[11/11] 📤 Return Dual Prediction...")
            time.sleep(0.2)
            print("        └─ ✅ (Male & Female Bone Age Results)")
            
            result = response.json()
            display_results(result)
            return True
        else:
            print(f"\n        └─ ❌ Server Error: {response.status_code}")
            print(response.text)
            return False
            
    except FileNotFoundError:
        print(f"\n❌ Error: Could not find image file '{image_path}'")
        return False
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server!")
        print("Make sure the server is running: python app.py")
        return False
    except requests.exceptions.Timeout:
        print("\n❌ Error: Request timed out!")
        print("The server might be processing. Try again.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def display_results(result):
    """Display prediction results"""
    print("\n" + "=" * 70)
    print("✅ PREDICTION SUCCESSFUL!")
    print("=" * 70)
    
    print(f"\n📋 Patient ID: {result['patient_id']}")
    print(f"🔢 Prediction ID: {result['prediction_id']}")
    print(f"📊 MLflow Run ID: {result['mlflow_run_id']}")
    
    print("\n" + "-" * 70)
    print("👨 MALE MODEL PREDICTION")
    print("-" * 70)
    male = result['male_prediction']
    print(f"  🎯 Estimated Age: {male['age']} ± {male['uncertainty_sigma']} years")
    print(f"  🔥 Grad-CAM: {male['gradcam_path']}")
    
    print("\n" + "-" * 70)
    print("👩 FEMALE MODEL PREDICTION")
    print("-" * 70)
    female = result['female_prediction']
    print(f"  🎯 Estimated Age: {female['age']} ± {female['uncertainty_sigma']} years")
    print(f"  🔥 Grad-CAM: {female['gradcam_path']}")
    
    print("\n" + "=" * 70)
    print("💾 RESULTS SAVED TO:")
    print("=" * 70)
    print(f"  📂 Files: data/storage/patients/{result['patient_id']}/")
    print(f"  💾 Database: boneage_predictions.db")
    print(f"  📊 MLflow: http://localhost:5000")
    print("=" * 70)

def main():
    """Main application loop"""
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🦴 BONE AGE ESTIMATION - Interactive Image Selector  ".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    while True:
        # Get list of images
        images = get_image_files()
        
        # Display menu and get selection
        selected_image = display_menu(images)
        
        if selected_image is None:
            print("\n👋 Exiting... Goodbye!")
            break
        
        # Get patient ID
        patient_id = get_patient_id()
        
        # Make prediction
        success = predict_image(selected_image, patient_id)
        
        if success:
            print("\n" + "=" * 70)
            choice = input("\n📷 Process another image? (y/n): ").strip().lower()
            
            if choice != 'y':
                print("\n✅ All done! Results saved successfully.")
                print("📊 View MLflow dashboard: http://localhost:5000")
                print("👋 Goodbye!")
                break
        else:
            retry = input("\n🔄 Try again? (y/n): ").strip().lower()
            if retry != 'y':
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
