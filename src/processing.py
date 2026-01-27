import pandas as pd
from src.database import get_engine

def get_employee_by_id(emp_id: int) -> pd.DataFrame:
    """Cherche un employé dans SQL via Pandas"""
    engine = get_engine()
    query = f"SELECT * FROM employees WHERE EmployeeNumber = {emp_id}"
    return pd.read_sql(query, con=engine)

def get_company_stats():
    """Prépare toutes les données pour les graphiques globaux."""
    engine = get_engine()
    query_base = """
        SELECT Department, JobRole, Age, MonthlyIncome, JobSatisfaction, 
               WorkLifeBalance, Attrition, OverTime 
        FROM employees
    """
    return pd.read_sql(query_base, con=engine)

def get_age_pyramid_data():
    """Données pour la pyramide des âges par tranches de 10 ans"""
    engine = get_engine()
    query = """
    SELECT (Age/10)*10 as Tranche_Age, Gender, COUNT(*) as Effectif
    FROM employees
    GROUP BY Tranche_Age, Gender
    """
    return pd.read_sql(query, con=engine)

def predict_attrition_risk(emp_data: dict) -> dict:
    """Calcule un score de risque prédictif sur 100."""
    score = 0
    if emp_data.get('OverTime') == 'Yes': score += 35
    if emp_data.get('JobSatisfaction', 4) < 2: score += 20
    # On ajoute une valeur par défaut de 0 si la clé n'existe pas
    if emp_data.get('YearsSinceLastPromotion', 0) > 3: score += 20
    if emp_data.get('MonthlyIncome', 5000) < 4000: score += 25
    
    score = min(score, 100)
    level = "Faible"
    color = "green"
    if score > 40: level, color = "Modéré", "orange"
    if score > 70: level, color = "Critique", "red"
    
    return {"score": score, "level": level, "color": color}

def calculate_impact(original_score, increase):
    """Simulateur d'impact d'augmentation."""
    reduction = (increase / 500) * 8
    return max(0, round(original_score - reduction, 1))