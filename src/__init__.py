import sys
import os
import sqlalchemy

# On s'assure que Python voit le dossier 'src'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.database import get_engine

def setup_security():
    engine = get_engine()
    print("Connexion à la base de données en cours...")
    
    # Utilisation de text() pour les versions récentes de SQLAlchemy
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)"))
        conn.commit() # On valide la création
        print("✅ La table 'users' a été créée avec succès dans la base SQL.")

if __name__ == "__main__":
    setup_security()