from fastapi import FastAPI, HTTPException
import sqlite3
import logging
from typing import List
import sys
from pathlib import Path

# Ajout du dossier parent au chemin pour importer les modules dans /src [cite: 22, 32]
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.models import EmployeeBase, EvaluationCreate, UserLogin

# Configuration du logging au lieu de print() [cite: 68]
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PerformTrack API")

# Chemin vers la base SQL [cite: 19, 45]
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "hr_database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API PerformTrack RH"}

# 1. Route pour l'authentification (Traçabilité demandée)
@app.post("/login")
def login(user: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    db_user = cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", 
        (user.username, user.password)
    ).fetchone()
    conn.close()
    
    if db_user:
        logger.info(f"Connexion réussie pour l'agent : {user.username}") [cite: 68, 85]
        # On s'assure de retourner les noms de colonnes corrects de la base SQL
        return {
            "status": "success", 
            "user_id": db_user["id"], 
            "full_name": db_user["full_name"]
        }
    raise HTTPException(status_code=401, detail="Identifiants incorrects") [cite: 86]

# 2. Route pour récupérer les employés (Dataset IBM)
@app.get("/employees", response_model=List[EmployeeBase])
def get_employees():
    conn = get_db_connection()
    # On limite à 100 pour la performance, comme suggéré [cite: 11]
    employees = conn.execute("SELECT * FROM employees LIMIT 100").fetchall()
    conn.close()
    return [dict(emp) for emp in employees]

# 3. Route pour soumettre une évaluation (Traçabilité)
@app.post("/evaluate")
def create_evaluation(eval_data: EvaluationCreate, agent_id: int):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO evaluations (employee_id, rh_agent_id, performance_score, comments) VALUES (?, ?, ?, ?)",
            (eval_data.employee_id, agent_id, eval_data.performance_score, eval_data.comments)
        )
        conn.commit()
        logger.info(f"Évaluation enregistrée par l'agent {agent_id}") [cite: 68]
        return {"message": "Évaluation enregistrée avec succès"}
    except Exception as e:
        logger.error(f"Erreur : {e}") [cite: 86]
        raise HTTPException(status_code=500, detail="Erreur interne de la base de données")
    finally:
        conn.close()