from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Modèle pour l'Authentification (Traçabilité)
class UserLogin(BaseModel):
    username: str
    password: str

# Modèle pour l'affichage d'un employé (Données IBM)
class EmployeeBase(BaseModel):
    emp_id: int
    Age: int
    JobRole: str
    Department: str
    MonthlyIncome: int
    PerformanceRating: int

# Modèle pour la nouvelle évaluation (Traçabilité)
class EvaluationCreate(BaseModel):
    employee_id: int
    performance_score: int
    comments: Optional[str] = None

# Modèle pour l'historique que le RH verra
class EvaluationOut(EvaluationCreate):
    id: int
    rh_agent_id: int
    date_scored: datetime

    class Config:
        from_attributes = True