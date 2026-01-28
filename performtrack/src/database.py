import pandas as pd
import sqlite3
import os
from pathlib import Path

# --- Configuration des chemins ---
# On remonte d'un niveau car le script est dans /src
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "processed" / "hr_database.db"
CSV_PATH = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"

def init_db():
    """Initialise la base de données SQL avec les données IBM et la table Users."""
    
    # Vérification de l'existence du fichier CSV
    if not CSV_PATH.exists():
        print(f"Erreur : Le fichier CSV est introuvable à l'adresse : {CSV_PATH}")
        return

    # 1. Connexion à SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 2. Chargement et nettoyage avec Pandas 
        print("Chargement des données IBM...")
        df = pd.read_csv(CSV_PATH)
        
        # Suppression des colonnes inutiles pour l'analyse de performance
        cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours']
        df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
        
        # 3. Création de la table 'employees'
        df.to_sql('employees', conn, if_exists='replace', index_label='emp_id')
        print(f"Table 'employees' créée avec {len(df)} lignes.")

        # 4. Création de la table 'users' (pour la traçabilité RH)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT
            )
        ''')

        # 5. Création d'une table 'evaluations' (pour l'historique des notes)
        # Cette table lie un employé, une note, et l'agent RH qui l'a donnée
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                rh_agent_id INTEGER,
                performance_score INTEGER,
                comments TEXT,
                date_scored DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (rh_agent_id) REFERENCES users (id)
            )
        ''')

        # 6. Ajout d'un compte RH par défaut (admin / admin123)
        # Note : En production, on utiliserait un hash de mot de passe
        try:
            cursor.execute(
                "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                ('admin', 'admin123', 'Responsable RH')
            )
        except sqlite3.IntegrityError:
            pass # L'utilisateur existe déjà

        conn.commit()
        print("✅ Base de données initialisée avec succès !")
        print(f"📍 Fichier généré : {DB_PATH}")

    except Exception as e:
        print(f"❌ Une erreur est survenue : {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()