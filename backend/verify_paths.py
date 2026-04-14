"""
Simple verification script to check database paths
"""

import sqlite3

def verify_database():
    """Verify all paths use forward slashes"""
    print("=" * 70)
    print("🔍 DATABASE PATH VERIFICATION")
    print("=" * 70)
    
    conn = sqlite3.connect('boneage_predictions.db')
    cursor = conn.cursor()
    
    # Check patients table
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM patients WHERE image_path LIKE '%\\%'")
    backslash_patients = cursor.fetchone()[0]
    
    # Check predictions table
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE male_gradcam_path LIKE '%\\%' OR female_gradcam_path LIKE '%\\%'")
    backslash_predictions = cursor.fetchone()[0]
    
    # Get sample paths
    cursor.execute("SELECT patient_id, image_path FROM patients LIMIT 3")
    sample_patients = cursor.fetchall()
    
    cursor.execute("SELECT male_gradcam_path, female_gradcam_path FROM predictions LIMIT 3")
    sample_predictions = cursor.fetchall()
    
    conn.close()
    
    # Display results
    print(f"\n📊 Database Statistics:")
    print(f"   Total patients: {total_patients}")
    print(f"   Total predictions: {total_predictions}")
    print(f"\n🔍 Path Analysis:")
    print(f"   Patients with backslashes: {backslash_patients}/{total_patients}")
    print(f"   Predictions with backslashes: {backslash_predictions}/{total_predictions}")
    
    if sample_patients:
        print(f"\n📋 Sample Patient Paths:")
        for patient_id, path in sample_patients:
            has_backslash = '\\' in path
            status = "❌" if has_backslash else "✅"
            print(f"   {status} {patient_id}: {path}")
    
    if sample_predictions:
        print(f"\n📋 Sample Prediction Paths:")
        for i, (male_path, female_path) in enumerate(sample_predictions, 1):
            if male_path:
                has_backslash = '\\' in male_path
                status = "❌" if has_backslash else "✅"
                print(f"   {status} Prediction {i} (Male): {male_path}")
            if female_path:
                has_backslash = '\\' in female_path
                status = "❌" if has_backslash else "✅"
                print(f"   {status} Prediction {i} (Female): {female_path}")
    
    # Final verdict
    print("\n" + "=" * 70)
    if backslash_patients == 0 and backslash_predictions == 0:
        print("✅ VERIFICATION PASSED!")
        print("   All paths use forward slashes for cross-platform compatibility")
        print("   Your application is ready to run on any operating system!")
    else:
        print("❌ VERIFICATION FAILED!")
        print(f"   Found {backslash_patients + backslash_predictions} paths with backslashes")
        print("   Please run: python migrate_database_paths.py")
    print("=" * 70)
    
    return backslash_patients == 0 and backslash_predictions == 0


if __name__ == "__main__":
    print("\n🦴 Bone Age Detection - Database Path Verification\n")
    success = verify_database()
    exit(0 if success else 1)
