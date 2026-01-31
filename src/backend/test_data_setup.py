"""
Script to setup test data for the application.
Creates a dummy CSV and initializes the SQLite database for testing.
"""
import os
import csv
import tempfile
import sqlite3
from unittest import mock

from data_setup import setup_db


def create_sample_csv(path):
    """
    Creates a dummy CSV file with sample employee data for testing purposes.
    """
    csv_file = os.path.join(path, "WA_Fn-UseC_-HR-Employee-Attrition.csv")
    rows = [
        {"EmployeeNumber": 1, "Age": 30, "Attrition": "No"},
        {"EmployeeNumber": 2, "Age": 40, "Attrition": "Yes"},
    ]
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["EmployeeNumber", "Age", "Attrition"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return csv_file


def main():
    """
    Main execution function for test data setup.
    Mocks the kaggle download and verifies database creation.
    """
    # Create a temporary directory that will act as the kaggle download folder
    with tempfile.TemporaryDirectory() as tmp:
        create_sample_csv(tmp)

        # Patch the dataset_download function used in data_setup to return our temp dir
        with mock.patch("data_setup.kagglehub.dataset_download", return_value=tmp):
            old_cwd = os.getcwd()
            try:
                # Change cwd so the sqlite file is created inside the temp dir
                os.chdir(tmp)
                setup_db()

                # Open the created sqlite DB and print the 'employees' table
                db_path = os.path.join(tmp, "hr_database.db")
                if not os.path.exists(db_path):
                    print("Error: hr_database.db not created")
                    return

                conn = sqlite3.connect(db_path)
                try:
                    cur = conn.cursor()
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees'")
                    if cur.fetchone() is None:
                        print("Error: table 'employees' not found in database")
                        return

                    # Fetch and display rows
                    cur.execute("SELECT * FROM employees")
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description]
                    print("Table 'employees' (columns = {}):".format(cols))
                    for r in rows:
                        print(dict(zip(cols, r)))
                finally:
                    conn.close()
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    main()
