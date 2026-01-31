"""
Migration script to add evaluation_note and comment columns
to the employees table if they do not already exist.
"""
import sqlite3
from pathlib import Path

def migrate_database():
    """Adds evaluation_note and comment columns to the employees table."""
    db_path = Path(__file__).resolve().parent.parent.parent / "data" / "hr_database.db"
    
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        print("The database will be created automatically on next startup.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(employees)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add evaluation_note if it doesn't exist
        if 'evaluation_note' not in columns:
            print("Adding column 'evaluation_note'...")
            cursor.execute("ALTER TABLE employees ADD COLUMN evaluation_note REAL")
            print("✓ Column 'evaluation_note' added successfully.")
        else:
            print("✓ Column 'evaluation_note' already exists.")
        
        # Add comment if it doesn't exist
        if 'comment' not in columns:
            print("Adding column 'comment'...")
            cursor.execute("ALTER TABLE employees ADD COLUMN comment TEXT")
            print("✓ Column 'comment' added successfully.")
        else:
            print("✓ Column 'comment' already exists.")
        
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
