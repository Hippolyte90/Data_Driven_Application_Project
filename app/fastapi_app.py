"""
Main FastAPI application module.
Defines API endpoints for authentication, employee data retrieval, and updates.
"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.backend.database import SessionLocal, engine, Base
from src.backend import database, models, crud, data_setup
from src.backend.migrate_db import migrate_database
import pandas as pd

Base.metadata.create_all(bind=engine)
# Migrate the database to add new columns
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
         summary="API Health Check",
         description="Root endpoint to verify that the API is up and running.",
         response_description="A welcome message indicating the API status.",
         operation_id="health_check",
         tags = ["monitoring"]
         )

async def root():
    """
    Root endpoint to check API health.
    Returns a welcome message indicating the API is running.
    """
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
    """
    Registers a new HR user.
    Checks if the email already exists before creating the user.
    """
    if crud.get_rh_user(db, data['email']):
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud.create_rh_user(db, data['email'], data['password'])



@app.post("/login",
          summary="Login RH User",
          description="Authenticate an RH user using email and password.",
          response_description="Login status and message.",
          operation_id="login_rh_user",
          tags=["authentication"]
          )
def login(data: dict, db: Session = Depends(get_db)):
    """
    Authenticates an HR user.
    Verifies email and password against the database.
    """
    user = crud.get_rh_user(db, data['email'])
    if not user or user.password != data['password']:
        return {"status": "error", "message": "Incorrect credentials. Please sign up or try again."}
    return {"status": "success"}



@app.get("/employee",
         summary="Get All Employees",
         description="Retrieve a list of all employees in the database.",
         response_description="List of employee objects.",
         operation_id="get_all_employees",
         tags=["employees"]
         )
def read_employees(db: Session = Depends(get_db)):
    """
    Retrieves a list of all employees.
    """
    emp = crud.get_employee_data(db)
    if not emp: raise HTTPException(status_code=404, detail="Employee data not found")
    return emp



@app.get("/employee/{emp_id}",
         summary="Get Employee by ID",
         description="Retrieve detailed information for a specific employee by their ID.",
         response_description="Employee object.",
         operation_id="get_employee_by_id",
         tags=["employees"]
         )
def read_employee(emp_id: int, db: Session = Depends(get_db)):
    """
    Retrieves detailed information for a specific employee by ID.
    """
    emp = crud.get_employee(db, emp_id)
    if not emp: raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@app.get("/sales",
         summary="Get Sales Department Data",
         description="Retrieve all employees belonging to the Sales department.",
         response_description="List of employees in Sales.",
         operation_id="get_sales_data",
         tags=["departments"]
         )
def get_sales_data(db: Session = Depends(get_db)):
    """
    Retrieves data for all employees in the Sales department.
    """
    sale_data = crud.get_data_sales_department(db)
    if not sale_data:
        raise HTTPException(status_code=404, detail="Sales department data not found")
    return sale_data


# Function to get statistics for Sales department
@app.get("/sales/sales_stats",
         summary="Get Sales Department Statistics",
         description="Calculate key statistics (total employees, attrition rate, satisfaction) for Sales.",
         response_description="Statistics object for Sales.",
         operation_id="get_sales_stats",
         tags=["analytics"]
         )
def get_sales_stats(db: Session = Depends(get_db)):
    """
    Calculates and returns key statistics for the Sales department:
    Total employees, Attrition rate, and Average Job Satisfaction.
    """
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



@app.get("/rd",
         summary="Get R&D Department Data",
         description="Retrieve all employees belonging to the Research & Development department.",
         response_description="List of employees in R&D.",
         operation_id="get_rd_data",
         tags=["departments"]
         )
def get_rd_data(db: Session = Depends(get_db)):
    """
    Retrieves data for all employees in the Research & Development department.
    """
    rd_data = crud.get_data_rd_department(db)
    if not rd_data:
        raise HTTPException(status_code=404, detail="R&D department data not found")
    return rd_data


# Function to get statistics for R&D department
@app.get("/rd/rd_stats",
         summary="Get R&D Department Statistics",
         description="Calculate key statistics (total employees, attrition rate, satisfaction) for R&D.",
         response_description="Statistics object for R&D.",
         operation_id="get_rd_stats",
         tags=["analytics"]
         )
def get_rd_stats(db: Session = Depends(get_db)):
    """
    Calculates and returns key statistics for the R&D department:
    Total employees, Attrition rate, and Average Job Satisfaction.
    """
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
    
        

@app.get("/hr",
         summary="Get HR Department Data",
         description="Retrieve all employees belonging to the Human Resources department.",
         response_description="List of employees in HR.",
         operation_id="get_hr_data",
         tags=["departments"]
         )
def get_hr_data(db: Session = Depends(get_db)):
    """
    Retrieves data for all employees in the Human Resources department.
    """
    hr_data = crud.get_data_hr_department(db)
    if not hr_data:
        raise HTTPException(status_code=404, detail="HR department data not found")
    return hr_data



# Function to get statistics for HR department
@app.get("/hr/hr_stats",
         summary="Get HR Department Statistics",
         description="Calculate key statistics (total employees, attrition rate, satisfaction) for HR.",
         response_description="Statistics object for HR.",
         operation_id="get_hr_stats",
         tags=["analytics"]
         )
def get_hr_stats(db: Session = Depends(get_db)):
    """
    Calculates and returns key statistics for the HR department:
    Total employees, Attrition rate, and Average Job Satisfaction.
    """
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
@app.get("/stats",
         summary="Get Global Statistics",
         description="Calculate global statistics (total employees, attrition rate, satisfaction) for the entire company.",
         response_description="Global statistics object.",
         operation_id="get_global_stats",
         tags=["analytics"]
         )
def get_stats(db: Session = Depends(get_db)):
    """
    Calculates and returns global statistics for the entire company:
    Total employees, Global Attrition rate, and Global Average Satisfaction.
    """
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

@app.post("/update_score",
          summary="Update Employee Score",
          description="Update the general performance score of an employee.",
          response_description="The updated employee record or status.",
          operation_id="update_employee_score",
          tags=["updates"]
          )
def update_score(data: dict, db: Session = Depends(get_db)):
    """
    Updates the general score of an employee.
    """
    return crud.update_employee_score(db, data['id'], data['score'])

@app.post("/update_evaluation_note",
          summary="Update Evaluation Note",
          description="Update the specific evaluation note (0-10) for an employee.",
          response_description="The updated employee record or status.",
          operation_id="update_evaluation_note",
          tags=["updates"]
          )
def update_evaluation_note(data: dict, db: Session = Depends(get_db)):
    """
    Updates the specific evaluation note (0-10) for an employee.
    """
    emp = crud.get_employee(db, data['id'])
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee_evaluation_note(db, data['id'], data['evaluation_note'])

@app.post("/update_comment",
          summary="Update Employee Comment",
          description="Update the textual comment/feedback for an employee.",
          response_description="The updated employee record or status.",
          operation_id="update_employee_comment",
          tags=["updates"]
          )
def update_comment(data: dict, db: Session = Depends(get_db)):
    """
    Updates the textual comment/feedback for an employee.
    """
    emp = crud.get_employee(db, data['id'])
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.update_employee_comment(db, data['id'], data['comment'])


@app.post("/add_employee",
          summary="Add New Employee",
          description="Register a new employee with comprehensive data, handling ID generation and validation.",
          response_description="Confirmation of creation and the new employee ID.",
          operation_id="add_new_employee",
          tags=["employees"]
          )
def add_employee(data: dict, db: Session = Depends(get_db)):
    """
    Registers a new employee with comprehensive data.
    Handles ID generation and validation.
    """
    # 1. ID Management
    if data.get("auto_id"):
        new_id = crud.get_max_id(db) + 1
    else:
        try:
            new_id = int(data.get("id"))
        except (TypeError, ValueError):
             raise HTTPException(status_code=400, detail="Invalid ID format.")

        # Check if ID already exists
        if crud.get_employee(db, new_id):
            raise HTTPException(status_code=400, detail=f"ID {new_id} already exists. Please choose another one.")
    
    # 2. Prepare Employee Data
    # Create a copy to avoid modifying the input dict directly
    emp_data = data.copy()
    
    # Remove auxiliary fields not present in the Employee model
    emp_data.pop("auto_id", None)
    
    # Assign the determined ID
    emp_data["id"] = new_id
    
    # Set default values for fields that might be missing or need initialization
    if "score" not in emp_data:
        emp_data["score"] = 0.0
        
    # Ensure Attrition is set (default to 'No' if missing)
    if "Attrition" not in emp_data:
        emp_data["Attrition"] = "No"
    
    # 3. Create and Save Employee
    try:
        # Unpack dictionary to create Employee instance
        # Note: Keys in emp_data must match Employee model columns
        new_emp = models.Employee(**emp_data)
        
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        
        return {
            "status": "success", 
            "id": new_id, 
            "message": "Employee successfully registered.",
            "data": emp_data
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")