"""
Script de migration pour ajouter les colonnes evaluation_note et comment
à la table employees si elles n'existent pas déjà.
"""
import sqlite3
from pathlib import Path

def migrate_database():
    """Ajoute les colonnes evaluation_note et comment à la table employees."""
    db_path = Path(__file__).resolve().parent.parent.parent / "data" / "hr_database.db"
    
    if not db_path.exists():
        print(f"Base de données introuvable: {db_path}")
        print("La base de données sera créée automatiquement au prochain démarrage.")
        return
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Vérifier si les colonnes existent déjà
        cursor.execute("PRAGMA table_info(employees)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Ajouter evaluation_note si elle n'existe pas
        if 'evaluation_note' not in columns:
            print("Ajout de la colonne 'evaluation_note'...")
            cursor.execute("ALTER TABLE employees ADD COLUMN evaluation_note REAL")
            print("✓ Colonne 'evaluation_note' ajoutée avec succès.")
        else:
            print("✓ Colonne 'evaluation_note' existe déjà.")
        
        # Ajouter comment si elle n'existe pas
        if 'comment' not in columns:
            print("Ajout de la colonne 'comment'...")
            cursor.execute("ALTER TABLE employees ADD COLUMN comment TEXT")
            print("✓ Colonne 'comment' ajoutée avec succès.")
        else:
            print("✓ Colonne 'comment' existe déjà.")
        
        conn.commit()
        print("\n✅ Migration terminée avec succès!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Erreur lors de la migration: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
