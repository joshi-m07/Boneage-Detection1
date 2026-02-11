# 🔧 Git Repository Cleanup & Publishing Guide

## ⚠️ Problem
The `male_boneage_model.pth` file (390 MB) is too large for GitHub and is blocking your push.

## ✅ Solution - Remove Model from Git History

### Step 1: Add .gitignore
**Already done!** ✅ Created `.gitignore` to exclude:
- `*.pth` - Model files
- `*.db` - Database files
- `mlruns/` - MLflow tracking
- `storage/` - Patient data

### Step 2: Remove Model from Git History

Run these commands in order:

```bash
# Navigate to your repo
cd "c:\Users\jayan\OneDrive\Desktop\Boneage Detection"

# Remove the model file from git tracking
git rm --cached male_boneage_model.pth

# Add the .gitignore
git add .gitignore

# Commit the changes
git commit -m "Remove large model file and add .gitignore"

# Remove from entire git history (this rewrites history)
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch male_boneage_model.pth" --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

### Step 3: Force Push (WARNING: This rewrites history)

```bash
# If you have a remote repository
git push origin main --force
```

---

## 🚀 Alternative: If You Haven't Pushed Yet

If you haven't pushed to GitHub yet, simpler approach:

```bash
# Remove from tracking
git rm --cached male_boneage_model.pth

# Add gitignore
git add .gitignore

# Amend the first commit
git add -A
git commit --amend -m "Initial commit - Backend implementation (model file excluded)"

# Now you can push normally
git push origin main
```

---

## 📝 What Files WILL Be Pushed

✅ **Code Files:**
- `app.py`
- `database/` folder
- `utils/` folder
- `male_boneage/male_boneage/` (code only)
- All `.py` scripts
- `requirements.txt`
- `README.md`, `SETUP.md`, etc.

❌ **Excluded Files:**
- `male_boneage_model.pth` (390 MB) 
- `female_boneage_model.pth`
- `boneage_predictions.db`
- `mlruns/` directory
- `storage/` directory
- `__pycache__/` folders

---

## 📦 Recommended: Store Model Separately

Since the model can't go on GitHub, store it:

1. **Google Drive / Dropbox** - Share link in README
2. **Git LFS** (Large File Storage) - If your GitHub account supports it
3. **Hugging Face Models** - Free model hosting
4. **Release Assets** - GitHub releases support larger files

Add to README:
```markdown
## Model Files

Download the model files separately:
- Male Model: [Download Link](your-link-here)
- Female Model: [Download Link](your-link-here)

Place them in the project root directory.
```

---

## 🎯 Quick Commands (Copy & Paste)

**Option 1: Clean History (if already committed)**
```bash
git rm --cached male_boneage_model.pth
git add .gitignore
git commit -m "Remove large model file and add .gitignore"
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch male_boneage_model.pth" --prune-empty --tag-name-filter cat -- --all
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin main --force
```

**Option 2: Amend First Commit (if not pushed yet)**
```bash
git rm --cached male_boneage_model.pth
git add .gitignore
git add -A
git commit --amend -m "Initial commit - Backend implementation (model excluded)"
git push origin main
```

---

## ✅ Verify Before Pushing

```bash
# Check what will be pushed
git ls-files | findstr .pth

# Should return nothing!

# Check repo size
git count-objects -vH

# Should be much smaller now
```

---

**Choose which option fits your situation and run those commands!** 🚀
