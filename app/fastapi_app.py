from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.backend.database import SessionLocal, engine, Base
from src.backend import database, models, crud, data_setup
from src.backend.migrate_db import migrate_database
import pandas as pd

Base.metadata.create_all(bind=engine)
# Migrer la base de données pour ajouter les nouvelles colonnes
migrate_database()
app = FastAPI(
    title="RH Performance and Attrition API",
    description="An API to retrieve employees information and performance.",
    version="0.1",
) 


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
    

# -- Endpoint to get movie details by ID ---
@app.get("/",
         summary="Get Employee Details by ID",
         description = "Retrieve detailed information about employees by providing its unique ID.",
         response_description="Detailed information about the employee.",
         operation_id="health_check_employee_api",
         tags = ["monitoring"]
         )

async def root():
    return {"message": "EmployeeTrack API is up and running!"} 


@app.post("/register",
            summary="Register RH User",
            description="Register a new RH user with email and password.",
            response_description="Details of the registered RH user.",
            operation_id="register_rh_user",
            tags = ["authentication"],
            #response_model=models.UserRH,
          )

def register(data: dict, db: Session = Depends(get_db)):
    if crud.get_rh_user(db, data['email']):
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_rh_user(db, data['email'], data['password'])



@app.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = crud.get_rh_user(db, data['email'])
    if not user or user.password != data['password']:
        return {"status": "error", "message": "Incorrect credentials. Please sign up or try again."}
    return {"status": "success"}



@app.get("/employee")
def read_employees(db: Session = Depends(get_db)):
    emp = crud.get_employee_data(db)
    if not emp: raise HTTPException(status_code=404, detail="Employee data not found")
    return emp



@app.get("/employee/{emp_id}")
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, emp_id)
    if not emp: raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.get("/sales")
def get_sales_data(db: Session = Depends(get_db)):
    sale_data = crud.get_data_sales_department(db)
    if not sale_data:
        raise HTTPException(status_code=404, detail="Sales department data not found")
    return sale_data


# Function to get statistics for Sales department
@app.get("/sales/sales_stats")
def get_sales_stats(db: Session = Depends(get_db)):
    sale_data = crud.get_data_sales_department(db)
    if not sale_data:
        raise HTTPException(status_code=404, detail="Sales department data not found")
    else:
        sale_dicts = [{'Attrition': emp.Attrition, 'JobSatisfaction': emp.JobSatisfaction} for emp in sale_data]
        sale_df = pd.DataFrame(sale_dicts)
        total_employees = len(sale_df)
        attrition_rate = (sale_df['Attrition'] == 'Yes').mean() * 100
        avg_satisfaction = sale_df['JobSatisfaction'].mean()
    return {
        "total_employees": total_employees,
        "attrition_rate": f"{attrition_rate:.2f}%",
        "average_job_satisfaction": f"{avg_satisfaction:.2f}/4"
    } 



@app.get("/rd")
def get_rd_data(db: Session = Depends(get_db)):
    rd_data = crud.get_data_rd_department(db)
    if not rd_data:
        raise HTTPException(status_code=404, detail="R&D department data not found")
    return rd_data


# Function to get statistics for R&D department
@app.get("/rd/rd_stats")
def get_rd_stats(db: Session = Depends(get_db)):
    rd_data = crud.get_data_rd_department(db)
    if not rd_data:
        raise HTTPException(status_code=404, detail="R&D department data not found")      
    else:
        rd_dicts = [{'Attrition': emp.Attrition, 'JobSatisfaction': emp.JobSatisfaction} for emp in rd_data]
        rd_df = pd.DataFrame(rd_dicts)
        total_employees = len(rd_df)
        attrition_rate = (rd_df['Attrition'] == 'Yes').mean() * 100
        avg_satisfaction = rd_df['JobSatisfaction'].mean()  
    return {    
        "total_employees": total_employees,
        "attrition_rate": f"{attrition_rate:.2f}%",
        "average_job_satisfaction": f"{avg_satisfaction:.2f}/4"
    }
    
        

@app.get("/hr")
def get_hr_data(db: Session = Depends(get_db)):
    hr_data = crud.get_data_hr_department(db)
    if not hr_data:
        raise HTTPException(status_code=404, detail="HR department data not found")
    return hr_data



# Function to get statistics for HR department
@app.get("/hr/hr_stats")
def get_hr_stats(db: Session = Depends(get_db)):
    hr_data = crud.get_data_hr_department(db)
    if not hr_data:
        raise HTTPException(status_code=404, detail="HR department data not found")     
    else:
        hr_dicts = [{'Attrition': emp.Attrition, 'JobSatisfaction': emp.JobSatisfaction} for emp in hr_data]
        hr_df = pd.DataFrame(hr_dicts)
        total_employees = len(hr_df)
        attrition_rate = (hr_df['Attrition'] == 'Yes').mean() * 100
        avg_satisfaction = hr_df['JobSatisfaction'].mean()
    return {    
        "total_employees": total_employees,
        "attrition_rate": f"{attrition_rate:.2f}%",
        "average_job_satisfaction": f"{avg_satisfaction:.2f}/4"
    }



# Global stat
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employee data found")
    else:
        # Convert ORM objects to list of dicts
        employee_dicts = [{
            'Attrition': emp.Attrition,
            'JobSatisfaction': emp.JobSatisfaction
        } for emp in employees]
        total_df = pd.DataFrame(employee_dicts)
        total_employees = len(total_df)
        attrition_rate = (total_df['Attrition'] == 'Yes').mean() * 100
        avg_satisfaction = total_df['JobSatisfaction'].mean()
    return {    
        "total": total_employees,
        "attrition": f"{attrition_rate:.2f}%",
        "satisfaction": f"{avg_satisfaction:.2f}/4"
    }




# @app.put("/employees/{employee_id}")
# def update_score(employee_id: int, score: float, db: Session = Depends(get_db)):
#     return crud.update_score(db, employee_id, score)

@app.post("/update_score")
def update_score(data: dict, db: Session = Depends(get_db)):
    return crud.update_employee_score(db, data['id'], data['score'])

@app.post("/update_evaluation_note")
def update_evaluation_note(data: dict, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, data['id'])
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee_evaluation_note(db, data['id'], data['evaluation_note'])

@app.post("/update_comment")
def update_comment(data: dict, db: Session = Depends(get_db)):
    emp = crud.get_employee(db, data['id'])
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee_comment(db, data['id'], data['comment'])


@app.post("/add_employee")
def add_employee(data: dict, db: Session = Depends(get_db)):
    # 1. Gestion de l'ID (Point 10)
    if data.get("auto_id"):
        new_id = crud.get_max_id(db) + 1
    else:
        new_id = data.get("id")
        # Vérification si l'ID existe déjà
        if crud.get_employee(db, new_id):
            raise HTTPException(status_code=400, detail="Cet ID existe déjà. Veuillez en choisir un autre.")
    
    # 2. Création de l'objet employé (avec valeurs par défaut pour les colonnes manquantes)
    new_emp = models.Employee(
        id=new_id,
        Age=data.get("Age", 30),
        Attrition="No",
        Department=data.get("Department", "R&D"),
        MonthlyIncome=data.get("MonthlyIncome", 3000),
        YearsAtCompany=data.get("YearsAtCompany", 0),
        JobSatisfaction=data.get("JobSatisfaction", 3),
        score=0.0  # Par défaut 0 comme demandé
    )
    
    db.add(new_emp)
    db.commit()
    return {"status": "success", "id": new_id}