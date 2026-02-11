"""
Test script to verify path normalization works correctly
"""

import os
import sys

def test_normalize_path():
    """Test the normalize_path_for_storage function"""
    # Import the function from app.py
    sys.path.insert(0, os.path.dirname(__file__))
    from app import normalize_path_for_storage
    
    print("=" * 70)
    print("🧪 TESTING PATH NORMALIZATION")
    print("=" * 70)
    
    test_cases = [
        ("storage\\patients\\TEST_001\\original.png", "storage/patients/TEST_001/original.png"),
        ("storage/patients/TEST_001/original.png", "storage/patients/TEST_001/original.png"),
        ("C:\\Users\\jayan\\Desktop\\file.png", "C:/Users/jayan/Desktop/file.png"),
        ("path/with/forward/slashes.png", "path/with/forward/slashes.png"),
    ]
    
    all_passed = True
    for input_path, expected_output in test_cases:
        result = normalize_path_for_storage(input_path)
        passed = result == expected_output
        all_passed = all_passed and passed
        
        status = "✅" if passed else "❌"
        print(f"\n{status} Test:")
        print(f"   Input:    {input_path}")
        print(f"   Expected: {expected_output}")
        print(f"   Got:      {result}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED!")
    print("=" * 70)
    
    return all_passed


def test_database_paths():
    """Verify database contains only normalized paths"""
    import sqlite3
    
    print("\n" + "=" * 70)
    print("🧪 TESTING DATABASE PATHS")
    print("=" * 70)
    
    conn = sqlite3.connect('boneage_predictions.db')
    cursor = conn.cursor()
    
    # Check for backslashes in patients table
    cursor.execute("SELECT COUNT(*) FROM patients WHERE image_path LIKE '%\\%'")
    backslash_patients = cursor.fetchone()[0]
    
    # Check for backslashes in predictions table
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE male_gradcam_path LIKE '%\\%' OR female_gradcam_path LIKE '%\\%'")
    backslash_predictions = cursor.fetchone()[0]
    
    # Get sample paths
    cursor.execute("SELECT image_path FROM patients LIMIT 3")
    sample_patient_paths = cursor.fetchall()
    
    cursor.execute("SELECT male_gradcam_path, female_gradcam_path FROM predictions LIMIT 3")
    sample_prediction_paths = cursor.fetchall()
    
    conn.close()
    
    print(f"\n📊 Results:")
    print(f"   Patients with backslashes: {backslash_patients}")
    print(f"   Predictions with backslashes: {backslash_predictions}")
    
    if sample_patient_paths:
        print(f"\n📋 Sample patient paths:")
        for path, in sample_patient_paths:
            print(f"   • {path}")
    
    if sample_prediction_paths:
        print(f"\n📋 Sample prediction paths:")
        for male_path, female_path in sample_prediction_paths:
            if male_path:
                print(f"   • Male: {male_path}")
            if female_path:
                print(f"   • Female: {female_path}")
    
    passed = backslash_patients == 0 and backslash_predictions == 0
    
    print("\n" + "=" * 70)
    if passed:
        print("✅ DATABASE VERIFICATION PASSED!")
        print("   All paths use forward slashes for cross-platform compatibility")
    else:
        print("❌ DATABASE VERIFICATION FAILED!")
        print(f"   Found {backslash_patients + backslash_predictions} paths with backslashes")
    print("=" * 70)
    
    return passed


if __name__ == "__main__":
    print("\n🦴 Bone Age Detection - Path Normalization Tests\n")
    
    # Run tests
    test1_passed = test_normalize_path()
    test2_passed = test_database_paths()
    
    # Final summary
    print("\n" + "=" * 70)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 70)
    print(f"   Path normalization function: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Database path verification:  {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print("=" * 70)
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Your application is cross-platform compatible.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED! Please review the errors above.")
        sys.exit(1)
