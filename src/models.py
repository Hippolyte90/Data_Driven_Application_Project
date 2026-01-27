from pydantic import BaseModel

class EmployeeResponse(BaseModel):
    EmployeeNumber: int
    Department: str
    JobRole: str
    MonthlyIncome: float
    PerformanceRating: int
    Attrition: str