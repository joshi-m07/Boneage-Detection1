# Setup Guide - Bone Age Estimation Backend

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-capable GPU for faster inference

## 🚀 Installation Steps

### Step 1: Install Dependencies

The backend requires several Python packages. Install them using pip:

```bash
pip install -r requirements.txt
```

**If you encounter issues**, try installing packages individually:

```bash
# Core web framework
pip install fastapi uvicorn[standard] python-multipart

# Machine Learning
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
# Or for CPU-only:
# pip install torch torchvision

# MLflow and data
pip install mlflow
pip install pillow opencv-python numpy matplotlib

# Database
pip install sqlalchemy

# Utilities
pip install pydantic aiofiles requests
```

### Step 2: Initialize Database

Create the database tables:

```bash
python -c "from database.db import init_db; init_db()"
```

You should see: `✓ Database initialized successfully`

### Step 3: Verify Model Files

Ensure you have the model file:
- ✅ `male_boneage_model.pth` (exists)
- ⚠️ `female_boneage_model.pth` (optional - will use male model if missing)

### Step 4: Start the Server

**Option A: Using the start script (Windows)**
```bash
start_server.bat
```

**Option B: Using Python directly**
```bash
python app.py
```

**Option C: Using uvicorn**
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The server will start on `http://localhost:8000`

### Step 5: Verify Installation

Open another terminal and run:

```bash
python test_api.py
```

Or manually test with curl:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "models": "loaded",
  "database": "connected",
  "mlflow": "initialized"
}
```

## 📡 Using the API

### Make a Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -F "image=@path/to/xray.png" \
  -F "patient_id=PATIENT_001"
```

### Get Patient Results

```bash
curl http://localhost:8000/results/PATIENT_001
```

### Interactive API Documentation

Open your browser to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 View MLflow Experiments

Start MLflow UI in a separate terminal:

```bash
mlflow ui
```

Then open: http://localhost:5000

## 📁 Directory Structure After Setup

```
Boneage Detection/
├── app.py                         # ✓ Created
├── requirements.txt               # ✓ Created
├── mlflow_config.py              # ✓ Created
├── start_server.bat              # ✓ Created
├── start_server.sh               # ✓ Created
├── test_api.py                   # ✓ Created
├── README.md                     # ✓ Created
├── boneage_predictions.db        # Created after first run
├── database/
│   ├── __init__.py               # ✓ Created
│   ├── db.py                     # ✓ Created
│   └── models.py                 # ✓ Created
├── utils/
│   ├── __init__.py               # ✓ Created
│   ├── inference.py              # ✓ Created
│   ├── gradcam_utils.py          # ✓ Created
│   └── augmentation.py           # ✓ Created
├── male_boneage/                 # Existing
│   └── male_boneage/
│       ├── model.py              # Existing
│       └── gradcam.py            # Existing
├── male_boneage_model.pth        # Existing
├── storage/                      # Created on first prediction
│   └── patients/
│       └── {patient_id}/
│           ├── original.png
│           ├── male_gradcam.png
│           └── female_gradcam.png
└── mlruns/                       # Created on first prediction
    └── ...                       # MLflow experiment data
```

## ⚠️ Troubleshooting

### PyTorch Installation Issues

If you have CUDA GPU:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

For CPU only:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Database Errors

Reset the database:
```bash
# Delete the database file
rm boneage_predictions.db  # Linux/Mac
del boneage_predictions.db  # Windows

# Reinitialize
python -c "from database.db import init_db; init_db()"
```

### MLflow Errors

Clear MLflow runs:
```bash
# Delete mlruns directory
rm -rf mlruns/       # Linux/Mac
rmdir /s mlruns      # Windows
```

### Import Errors

Make sure you're in the correct directory:
```bash
cd "c:\Users\jayan\OneDrive\Desktop\Boneage Detection"
```

### Port Already in Use

Change the port:
```bash
uvicorn app:app --port 8001
```

## 🎯 Quick Test

1. **Health check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Run test suite:**
   ```bash
   python test_api.py
   ```

3. **View API docs:**
   Open http://localhost:8000/docs in your browser

## 📝 Next Steps

1. ✅ All backend code is implemented
2. ⏳ Install dependencies (`pip install -r requirements.txt`)
3. ⏳ Start the server (`python app.py`)
4. ⏳ Test with sample X-ray images
5. ⏳ (Optional) Add female model weights for dual predictions

## 💡 Tips

- **GPU Acceleration:** The code automatically detects and uses GPU if available
- **Female Model:** Place `female_boneage_model.pth` in the project root for dual model predictions
- **Custom Database:** Edit `database/db.py` to use PostgreSQL or MySQL instead of SQLite
- **Remote MLflow:** Edit `mlflow_config.py` to use a remote tracking server

## 🔗 Resources

- FastAPI docs: https://fastapi.tiangolo.com/
- MLflow docs: https://mlflow.org/docs/latest/index.html
- PyTorch docs: https://pytorch.org/docs/stable/index.html

---

**Need help?** Check the [README.md](README.md) for detailed documentation or the [walkthrough.md](walkthrough.md) for implementation details.
