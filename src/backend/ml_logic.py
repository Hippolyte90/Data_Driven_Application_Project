import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Note: En production, le modèle devrait être pré-entraîné et sauvegardé (pickle)
def predict_attrition(employee_data, extra_years, extra_salary):
    # Logique simplifiée pour l'exemple
    # On ajuste les variables selon les entrées du RH
    current_income = employee_data['MonthlyIncome'] + extra_salary
    current_years = employee_data['YearsAtCompany'] + extra_years
    
    # Simulation de probabilité (à remplacer par un vrai modèle .predict())
    chance = 0.15 if current_income > 5000 else 0.45
    return "Partira" if chance > 0.4 else "Restera"