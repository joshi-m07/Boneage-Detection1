import sqlite3

conn = sqlite3.connect('boneage_predictions.db')
c = conn.cursor()

# Check for backslashes
c.execute('SELECT COUNT(*) FROM patients WHERE image_path LIKE "%\\%"')
patients_backslash = c.fetchone()[0]

c.execute('SELECT COUNT(*) FROM predictions WHERE male_gradcam_path LIKE "%\\%"  OR female_gradcam_path LIKE "%\\%"')
predictions_backslash = c.fetchone()[0]

# Get sample paths
c.execute('SELECT image_path FROM patients LIMIT 3')
sample_paths = c.fetchall()

print("=" * 70)
print("DATABASE VERIFICATION RESULTS")
print("=" * 70)
print(f"\nPatients with backslashes: {patients_backslash}")
print(f"Predictions with backslashes: {predictions_backslash}")
print(f"\nSample paths from database:")
for path, in sample_paths:
    print(f"  {path}")

if patients_backslash == 0 and predictions_backslash == 0:
    print("\n" + "=" * 70)
    print("SUCCESS! All paths use forward slashes.")
    print("Your application is now cross-platform compatible!")
    print("=" * 70)
else:
    print("\nERROR: Found backslashes in database!")

conn.close()
