"""
Database Path Migration Script
Converts all existing Windows-style paths (backslashes) to Unix-style paths (forward slashes)
for cross-platform compatibility.

Run this script once to fix existing database entries.
"""

import sqlite3
import os

def migrate_database_paths(db_path='boneage_predictions.db'):
    """
    Migrate all paths in the database to use forward slashes
    
    Args:
        db_path: Path to the SQLite database file
    """
    print("=" * 70)
    print("🔄 DATABASE PATH MIGRATION")
    print("=" * 70)
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Migrate patients table
        print("\n📋 Migrating 'patients' table...")
        cursor.execute("SELECT id, image_path FROM patients")
        patients = cursor.fetchall()
        
        patients_updated = 0
        for patient_id, image_path in patients:
            if image_path and '\\' in image_path:
                normalized_path = image_path.replace('\\', '/')
                cursor.execute(
                    "UPDATE patients SET image_path = ? WHERE id = ?",
                    (normalized_path, patient_id)
                )
                patients_updated += 1
                print(f"  ✓ Updated patient {patient_id}: {image_path} → {normalized_path}")
        
        print(f"\n✅ Updated {patients_updated} patient records")
        
        # Migrate predictions table
        print("\n📋 Migrating 'predictions' table...")
        cursor.execute("SELECT id, male_gradcam_path, female_gradcam_path FROM predictions")
        predictions = cursor.fetchall()
        
        predictions_updated = 0
        for pred_id, male_path, female_path in predictions:
            male_normalized = male_path.replace('\\', '/') if male_path and '\\' in male_path else male_path
            female_normalized = female_path.replace('\\', '/') if female_path and '\\' in female_path else female_path
            
            if male_normalized != male_path or female_normalized != female_path:
                cursor.execute(
                    "UPDATE predictions SET male_gradcam_path = ?, female_gradcam_path = ? WHERE id = ?",
                    (male_normalized, female_normalized, pred_id)
                )
                predictions_updated += 1
                if male_normalized != male_path:
                    print(f"  ✓ Updated prediction {pred_id} (male): {male_path} → {male_normalized}")
                if female_normalized != female_path:
                    print(f"  ✓ Updated prediction {pred_id} (female): {female_path} → {female_normalized}")
        
        print(f"\n✅ Updated {predictions_updated} prediction records")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\n📊 Summary:")
        print(f"  • Patients updated: {patients_updated}")
        print(f"  • Predictions updated: {predictions_updated}")
        print(f"  • Total records processed: {len(patients)} patients, {len(predictions)} predictions")
        print("\n✅ All paths now use forward slashes for cross-platform compatibility")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def verify_migration(db_path='boneage_predictions.db'):
    """
    Verify that all paths use forward slashes
    
    Args:
        db_path: Path to the SQLite database file
    """
    print("\n" + "=" * 70)
    print("🔍 VERIFYING MIGRATION")
    print("=" * 70)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check patients table
        cursor.execute("SELECT image_path FROM patients WHERE image_path LIKE '%\\%'")
        backslash_patients = cursor.fetchall()
        
        # Check predictions table
        cursor.execute("SELECT male_gradcam_path, female_gradcam_path FROM predictions WHERE male_gradcam_path LIKE '%\\%' OR female_gradcam_path LIKE '%\\%'")
        backslash_predictions = cursor.fetchall()
        
        if backslash_patients or backslash_predictions:
            print(f"❌ Found {len(backslash_patients)} patients and {len(backslash_predictions)} predictions with backslashes")
            return False
        else:
            print("✅ All paths verified - no backslashes found!")
            
            # Show sample paths
            cursor.execute("SELECT image_path FROM patients LIMIT 3")
            sample_paths = cursor.fetchall()
            if sample_paths:
                print("\n📋 Sample paths from database:")
                for path, in sample_paths:
                    print(f"  • {path}")
            
            return True
            
    finally:
        conn.close()


if __name__ == "__main__":
    print("\n🦴 Bone Age Detection - Database Path Migration\n")
    
    # Run migration
    migrate_database_paths()
    
    # Verify migration
    verify_migration()
    
    print("\n" + "=" * 70)
    print("🎉 Migration complete! Your database is now cross-platform compatible.")
    print("=" * 70)
