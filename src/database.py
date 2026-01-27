import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "data/processed/hr_database.db"
CSV_PATH = "data/raw/employees.csv"

def initialize_database():
    """Transforme le CSV en table SQL"""
    if not os.path.exists(CSV_PATH):
        print("Erreur : CSV introuvable !")
        return
    df = pd.read_csv(CSV_PATH)
    engine = create_engine(f'sqlite:///{DB_PATH}')
    df.to_sql('employees', con=engine, if_exists='replace', index=False)

def get_engine():
    """Retourne la connexion à la base"""
    return create_engine(f'sqlite:///{DB_PATH}')