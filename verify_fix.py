import requests
import time
import sys
import os

def verify():
    url = "http://localhost:8000/predict"
    image_path = "Bonepic.jpg"
    
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        sys.exit(1)

    print("Waiting for server to be ready...")
    for i in range(30):
        try:
            r = requests.get("http://localhost:8000/health", timeout=2)
            if r.status_code == 200:
                print("Server is up and healthy!")
                break
        except requests.exceptions.ConnectionError:
            time.sleep(2)
            print(".", end="", flush=True)
    else:
        print("\nServer failed to start in time or is not reachable.")
        sys.exit(1)

    print(f"\nSending prediction request with {image_path}...")
    try:
        with open(image_path, 'rb') as f:
            files = {'image': (image_path, f, 'image/jpeg')}
            data = {'patient_id': 'TEST_FIX_VERIFY'}
            response = requests.post(url, files=files, data=data, timeout=60)
            
        if response.status_code == 200:
            print("SUCCESS: Prediction returned 200 OK")
            result = response.json()
            print(f"Male Age: {result['male_prediction']['age']}")
            print(f"Female Age: {result['female_prediction']['age']}")
        else:
            print(f"FAILURE: Status {response.status_code}")
            print(response.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify()
