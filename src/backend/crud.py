from sqlalchemy.orm import Session
from . import models

def get_employee_data(db: Session):
    return db.query(models.Employee).all()

def get_employee(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()

def get_max_id(db: Session):
    max_id = db.query(models.Employee.id).order_by(models.Employee.id.desc()).first()
    return max_id[0] if max_id else 0

def create_rh_user(db: Session, email: str, password: str):
    db_user = models.UserRH(email=email, password=password)
    db.add(db_user)
    db.commit()
    return db_user

def get_rh_user(db: Session, email: str):
    return db.query(models.UserRH).filter(models.UserRH.email == email).first()

def update_employee_score(db: Session, emp_id: int, score: float):
    emp = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if emp:
        emp.score = score
        db.commit()
    return emp

def get_data_sales_department(db: Session):
    return db.query(models.Sales).all()

def get_data_rd_department(db: Session):
    return db.query(models.RD).all()

def get_data_hr_department(db: Session):
    return db.query(models.HR).all()