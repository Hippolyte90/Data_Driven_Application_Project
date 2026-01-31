import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Note: In production, the model should be pre-trained and saved (pickle)
def predict_attrition(employee_data, extra_years, extra_salary):
    """
    Simulates attrition prediction logic based on employee data and potential changes.
    
    Args:
        employee_data (dict): Dictionary containing current employee details.
        extra_years (int): Additional years at company to simulate.
        extra_salary (float): Additional salary amount to simulate.
        
    Returns:
        str: 'Partira' (Will leave) or 'Restera' (Will stay) based on the simulation.
    """
    # Simplified logic for the example
    # We adjust variables according to HR inputs
    current_income = employee_data['MonthlyIncome'] + extra_salary
    current_years = employee_data['YearsAtCompany'] + extra_years
    
    # Probability simulation (to be replaced by a real .predict() model)
    chance = 0.15 if current_income > 5000 else 0.45
    return "Partira" if chance > 0.4 else "Restera"