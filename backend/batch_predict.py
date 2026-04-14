import os
import requests
import json
from datetime import datetime
import time

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
                # Skip test images
                if file != 'test_xray.png':
                    files.append(file)
    
    return sorted(files)

def predict_image(image_path, patient_id):
    """Send prediction request to API"""
    try:
        with open(image_path, 'rb') as f:
            files = {'image': (image_path, f, 'image/jpeg')}
            data = {'patient_id': patient_id}
            
            response = requests.post(f"{API_URL}/predict", files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return None, str(e)

def main():
    """Batch process all images"""
    print("=" * 80)
    print("🦴 BONE AGE ESTIMATION - Batch Processor")
    print("=" * 80)
    
    # Get all images
    images = get_image_files()
    
    if not images:
        print("\n❌ No image files found!")
        return
    
    print(f"\n📸 Found {len(images)} image(s) to process:")
    for i, img in enumerate(images, 1):
        print(f"   {i}. {img}")
    
    confirm = input("\n🔄 Process all images? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cancelled.")
        return
    
    # Process each image
    results = []
    failed = []
    
    print("\n" + "=" * 80)
    print("⏳ PROCESSING IMAGES...")
    print("=" * 80)
    
    for i, image in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] Processing: {image}")
        
        # Generate patient ID from filename
        patient_id = f"BATCH_{os.path.splitext(image)[0]}_{datetime.now().strftime('%Y%m%d')}"
        
        result, error = predict_image(image, patient_id)
        
        if result:
            print(f"  ✅ Success! Male: {result['male_prediction']['age']} years, Female: {result['female_prediction']['age']} years")
            results.append({
                'image': image,
                'patient_id': patient_id,
                'result': result
            })
        else:
            print(f"  ❌ Failed: {error}")
            failed.append({
                'image': image,
                'error': error
            })
        
        # Small delay to not overwhelm the server
        if i < len(images):
            time.sleep(0.5)
    
    # Display summary
    print("\n" + "=" * 80)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 80)
    
    print(f"\n✅ Successful: {len(results)}/{len(images)}")
    print(f"❌ Failed: {len(failed)}/{len(images)}")
    
    if results:
        print("\n" + "-" * 80)
        print("SUCCESSFUL PREDICTIONS")
        print("-" * 80)
        
        for r in results:
            male_age = r['result']['male_prediction']['age']
            female_age = r['result']['female_prediction']['age']
            print(f"\n📸 {r['image']}")
            print(f"   Patient ID: {r['patient_id']}")
            print(f"   👨 Male: {male_age} years")
            print(f"   👩 Female: {female_age} years")
            print(f"   📂 Files: data/storage/patients/{r['patient_id']}/")
    
    if failed:
        print("\n" + "-" * 80)
        print("FAILED PREDICTIONS")
        print("-" * 80)
        
        for f in failed:
            print(f"\n❌ {f['image']}")
            print(f"   Error: {f['error']}")
    
    # Save summary to file
    summary_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total': len(images),
            'successful': len(results),
            'failed': len(failed),
            'results': results,
            'failures': failed
        }, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"💾 Summary saved to: {summary_file}")
    print("📊 View all experiments in MLflow: http://localhost:5000")
    print("=" * 80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
