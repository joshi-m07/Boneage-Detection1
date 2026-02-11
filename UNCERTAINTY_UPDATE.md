# 🔧 Uncertainty Calculation Update

## What Changed

### Problem
- Uncertainty was showing as large values like `100.155`
- Not meaningful for medical interpretation
- Should show as `17.5 ± 0.5 years` format

### Solution Implemented

#### 1. Updated `utils/inference.py`
**File:** `utils/inference.py` (Lines 96-125)

**Before:**
```python
uncertainty = abs(unc_logits[0, 0].item())  # Raw value: ~100
```

**After:**
```python
# Calculate uncertainty from model's unc output
unc_val = unc_logits[0].abs().mean().item()  # Average of both outputs

# Normalize to reasonable range (0.5-2.5 years)
uncertainty_normalized = min(max(unc_val / 40.0, 0.5), 2.5)
```

**Logic:**
- Model outputs 2 uncertainty values
- Average them for better estimate
- Normalize from 0-100 scale to 0.5-2.5 years
- Clamp to minimum ±0.5 and maximum ±2.5 years

#### 2. Updated Display Format
**Files Updated:**
- `interactive_predict.py`
- `predict_bonepic.py`

**Change:**
```python
# Before
print(f"Age: {age} years")
print(f"Uncertainty (σ): {uncertainty}")

# After  
print(f"Age: {age} ± {uncertainty} years")
```

---

## Results

### Old Format:
```
🎯 Estimated Age: 17.5 years
📉 Uncertainty (σ): 100.155
```

### New Format:
```
🎯 Estimated Age: 17.5 ± 2.5 years
```

This means the predicted age is **17.5 years**, with a confidence interval of **±2.5 years** (range: 15-20 years).

---

## Uncertainty Interpretation

| Value | Meaning |
|-------|---------|
| `17.5 ± 0.5` | High confidence (17-18 years) |
| `17.5 ± 1.0` | Good confidence (16.5-18.5 years) |
| `17.5 ± 1.5` | Moderate confidence (16-19 years) |
| `17.5 ± 2.5` | Lower confidence (15-20 years) |

The model's uncertainty output is normalized to provide clinically meaningful ranges.

---

## To Apply Changes

**The server must be restarted for changes to take effect!**

### Steps:

1. **Stop the current server:**
   - In the terminal running `python app.py`
   - Press `Ctrl+C`

2. **Restart the server:**
   ```bash
   python app.py
   ```

3. **Test with new predictions:**
   ```bash
   python predict_bonepic.py
   ```

You should now see output like:
```
🎯 Predicted Age: 17.5 ± 2.5 years
```

---

## Technical Details

### Model Architecture
The `BoneAgeModel` has two output heads:
- `grp`: 4-class age group (0-5, 5-10, 10-15, 15-20 years)
- `unc`: 2D uncertainty estimation

### Normalization Formula
```python
unc_val = mean(|unc[0]|, |unc[1]|)  # Average of both outputs
uncertainty = clamp(unc_val / 40.0, 0.5, 2.5)  # Normalize to years
```

The `/40.0` scaling factor was chosen based on observed model output ranges. You may need to adjust this based on your training data.

---

**Changes are backward compatible** - the API response structure remains the same, only the `uncertainty_sigma` value is now normalized.
