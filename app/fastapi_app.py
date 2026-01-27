from fastapi import FastAPI, HTTPException
from src.processing import get_employee_by_id

app = FastAPI(title="API RH Performance")

@app.get("/employee/{emp_id}")
async def read_employee(emp_id: int):
    result = get_employee_by_id(emp_id)
    if result.empty:
        raise HTTPException(status_code=404, detail="Employé non trouvé")
    return result.iloc[0].to_dict()