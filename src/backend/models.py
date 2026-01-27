from sqlalchemy import Column, Integer, String, Float
from .database import Base
from pydantic import BaseModel


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Attrition = Column(String)
    BusinessTravel = Column(String)
    DailyRate = Column(Integer)
    Department = Column(String)
    DistanceFromHome = Column(Integer)
    Education = Column(Integer)
    EducationField = Column(String)
    EnvironmentSatisfaction = Column(Integer)
    Gender = Column(String)
    HourlyRate = Column(Integer)
    JobInvolvement = Column(Integer)
    JobLevel = Column(Integer)
    JobRole = Column(String)
    JobSatisfaction = Column(Integer)
    MaritalStatus = Column(String)
    MonthlyIncome = Column(Integer)
    MonthlyRate = Column(Integer)
    NumCompaniesWorked = Column(Integer)
    OverTime = Column(String)
    PercentSalaryHike = Column(Integer)
    PerformanceRating = Column(Integer)
    RelationshipSatisfaction = Column(Integer)
    StandardHours = Column(Integer)
    StockOptionLevel = Column(Integer)
    TotalWorkingYears = Column(Integer)
    TrainingTimesLastYear = Column(Integer)
    WorkLifeBalance = Column(Integer)
    YearsAtCompany = Column(Integer)
    YearsInCurrentRole = Column(Integer)
    YearsSinceLastPromotion = Column(Integer)
    YearsWithCurrManager = Column(Integer)
    score = Column(Float, default=0.0)

class UserRH(Base):
    __tablename__ = "users_rh"
    email = Column(String, primary_key=True, index=True)
    password = Column(String) # En production, utilisez un hash
    
class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Attrition = Column(String)
    Education = Column(Integer)
    JobRole = Column(String)
    MonthlyIncome = Column(Integer)
    EnvironmentSatisfaction = Column(Integer)
    JobInvolvement = Column(Integer)
    RelationshipSatisfaction = Column(Integer)
    PerformanceRating = Column(Integer)
    JobSatisfaction = Column(Integer)
    WorkLifeBalance = Column(Integer)
    
class RD(Base):
    __tablename__ = "RD"
    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Attrition = Column(String)
    Education = Column(Integer)
    JobRole = Column(String)
    MonthlyIncome = Column(Integer)
    EnvironmentSatisfaction = Column(Integer)
    JobInvolvement = Column(Integer)
    RelationshipSatisfaction = Column(Integer)
    PerformanceRating = Column(Integer)
    JobSatisfaction = Column(Integer)
    WorkLifeBalance = Column(Integer)
    
class HR(Base):
    __tablename__ = "HR"
    id = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Attrition = Column(String)
    Education = Column(Integer)
    JobRole = Column(String)
    MonthlyIncome = Column(Integer)
    EnvironmentSatisfaction = Column(Integer)
    JobInvolvement = Column(Integer)
    RelationshipSatisfaction = Column(Integer)
    PerformanceRating = Column(Integer)
    JobSatisfaction = Column(Integer)
    WorkLifeBalance = Column(Integer)