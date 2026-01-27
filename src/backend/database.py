import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .data_setup import setup_db
from pathlib import Path


# Allow overriding via env var, otherwise point to the project's parent `data` folder
env_db = os.getenv("DATABASE_URL")
if env_db:
	SQLALCHEMY_DATABASE_URL = env_db
else:
	db_path = Path(__file__).resolve().parent.parent.parent / "data" / "hr_database.db"
	# # project root is parent of `app` folder
	# backend_dir = os.path.dirname(os.path.abspath(__file__))
	# project_root = os.path.dirname(os.path.dirname(os.path.dirname(backend_dir)))
	# data_dir = os.path.join(project_root, "data")
	# print(data_dir)
	# #print(f"DATA DIR:{data_dir}")
    
	# # ensure data dir exists (no-op if it does)
	try:
		#os.makedirs(data_dir, exist_ok=True)
		setup_db()
	except Exception:
		pass
	#db_path = os.path.join(data_dir, "hr_database.db")
	SQLALCHEMY_DATABASE_URL = f"sqlite:////{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Quick helper for debugging (uncomment if needed)
# if __name__ == '__main__':
#      print('Using DB:', SQLALCHEMY_DATABASE_URL)