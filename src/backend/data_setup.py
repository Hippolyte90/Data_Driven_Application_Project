import kagglehub
import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine

#  Useful colomns
useful_cols = ['id','Age', 'Attrition',
               'Department', 'Education', 'JobRole', 
                'MonthlyIncome', 'EnvironmentSatisfaction',
                'JobInvolvement', 'RelationshipSatisfaction', 
                'PerformanceRating', 'JobSatisfaction','WorkLifeBalance']

organized_cols = [col for col in useful_cols if col != "Department"]

# Function to retrieve the useful part of the dataset specific for each department
def data_department(department_name, data_df):
    use_df = data_df[useful_cols]
    data_dep =  use_df[use_df["Department"] == department_name]
    data_dep = data_dep.reset_index(drop=True)
    data_dep = data_dep.drop(columns=["Department"])
    data_dep = data_dep[organized_cols]
    return data_dep

def setup_db():
    print("Downloading data...")
    path = kagglehub.dataset_download("pavansubhasht/ibm-hr-analytics-attrition-dataset")
    csv_file = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    # define the database path
    db_path = Path(__file__).resolve().parent.parent.parent / "data" / "hr_database.db"
    print(db_path)
    csv_path = os.path.join(path, csv_file)
    df = pd.read_csv(csv_path)
    
    # Added default evaluation score, evaluation note and comments column for HR.
    df['score'] = 0.0
    df['evaluation_note'] = None
    df['comment'] = ""
    
    # We use EmployeeNumber as the ID
    df = df.rename(columns={'EmployeeNumber': 'id'})
    
    # Ensure parent directory exists so SQLite can create the file
    db_path.parent.mkdir(parents=True, exist_ok=True)
    engine = create_engine('sqlite:////' + str(db_path))
    if df.to_sql('employees', engine, if_exists='replace', index=False):
        print(f"'hr_database.db' database created with {len(df)} employees.")
        
    else:
        print("Error creating the database.")
    
    # Sales department
    sales_df = data_department("Sales", df)
    
    if sales_df.to_sql('sales', engine, if_exists='replace', index=False):
        print(f"Sales table created with {len(sales_df)} employees.")
    else:
        print("Error creating the Sales table.")
    
    # Research & Development department
    rnd_df = data_department("Research & Development", df)
    if rnd_df.to_sql('RD', engine, if_exists='replace', index=False):
        print(f"RD table created with {len(rnd_df)} employees.")
    else:
        print("Error creating the RD table.")
    
    # Human Resources department
    hr_df = data_department("Human Resources", df)
    if hr_df.to_sql('HR', engine, if_exists='replace', index=False):
        print(f"HR table created with {len(hr_df)} employees.")
    else:
        print("Error creating the HR table.")
if __name__ == "__main__":
    setup_db()