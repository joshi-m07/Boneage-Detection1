# 🦴 Quick Start Guide - Interactive Image Selection

## 🚀 How to Use

### Step 1: Start the Backend Server
```bash
python app.py
```
Leave this running!

### Step 2: Run the Interactive Tool
Open a **new terminal** and run:
```bash
python interactive_predict.py
```

### Step 3: Select Your Image
You'll see a menu like this:
```
======================================================================
🖼️  AVAILABLE X-RAY IMAGES
======================================================================
  [1] Bonepic.jpg                              (8.8 KB)
  [2] test_xray.png                            (253.8 KB)
  [0] Exit
======================================================================

👉 Select image number: _
```

**Type the number** of the image you want to analyze and press Enter.

### Step 4: Enter Patient ID
```
👤 Enter Patient ID (press Enter for 'PATIENT_20260203_200544'): _
```

- Type a custom ID (e.g., `PATIENT_001`)
- Or just press **Enter** to use the auto-generated one

### Step 5: View Results
The tool will show:
- ✅ Male model prediction (age + uncertainty)
- ✅ Female model prediction (age + uncertainty)
- ✅ Where files are saved
- ✅ MLflow tracking info

### Step 6: Process Another or Exit
```
📷 Process another image? (y/n): _
```

- Type `y` to select another image
- Type `n` to exit

---

## 📋 Features

✅ **Auto-detects** all image files in the folder  
✅ **Shows file sizes** for each image  
✅ **Auto-generates** patient IDs with timestamps  
✅ **Custom patient IDs** - enter your own  
✅ **Beautiful output** with emojis and formatting  
✅ **Process multiple** images in one session  
✅ **Error handling** - clear messages if something goes wrong  

---

## 💡 Tips

1. **Add images to the folder** - The tool finds all `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff` files

2. **Keep the server running** - Make sure `python app.py` is running in another terminal

3. **View MLflow dashboard** - Open http://localhost:5000 to see all experiments

4. **Check database** - All results are saved in `boneage_predictions.db`

5. **Find visualizations** - Grad-CAM heatmaps are in `storage/patients/{patient_id}/`

---

## 🎯 Example Session

```
🖼️  AVAILABLE X-RAY IMAGES
  [1] Bonepic.jpg
  [2] hand_xray_1.png
  [3] wrist_scan.jpg
  [0] Exit

👉 Select image number: 1
👤 Enter Patient ID: JOHN_DOE_001

✅ PREDICTION SUCCESSFUL!
📋 Patient ID: JOHN_DOE_001
👨 MALE MODEL: 17.5 years (σ: 100.155)
👩 FEMALE MODEL: 17.5 years (σ: 100.155)

📷 Process another image? (y/n): y

👉 Select image number: 2
...
```

---

## 🛠️ Troubleshooting

**"Cannot connect to API server"**
→ Make sure `python app.py` is running

**"No image files found"**
→ Add some X-ray images to the folder

**"Error 500"**
→ Check if model files exist (`male_boneage_model.pth`)

---

## 📂 File Structure

```
Boneage Detection/
├── interactive_predict.py    ← Run this!
├── app.py                     ← Keep this running
├── Bonepic.jpg               ← Your images
├── hand_xray.png             ← Your images
└── storage/patients/         ← Results saved here
```

---

**Enjoy effortless bone age estimation! 🦴✨**
