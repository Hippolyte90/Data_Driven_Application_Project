# ↗️ HR Management System - Perform Employee Track

Welcome to the **HR Management System**, a comprehensive human resources management application designed to track employee performance, analyze attrition, and visualize key performance indicators (KPIs).

This project combines a robust backend API using **FastAPI** and an interactive user interface using **Streamlit**.

## 📋 Features

- **Secure Authentication**: Sign up and login for HR managers.
- **Interactive Dashboard**: Visualization of global KPIs, attrition rates, average satisfaction, and charts by department.
- **Employee Management**:
  - Add new employees with a comprehensive form.
  - Search for employees by ID.
  - Update evaluation ratings and comments.
- **Department Views**: Specific dashboards for Sales, R&D, and Human Resources.
- **Multilingual Support**: Interface available in **English** and **French** (hybrid translation: manual dictionary + Helsinki NLP model).
- **API Documentation**: Automatic documentation via Swagger UI.

## 🛠️ Tech Stack

- **Frontend** : [Streamlit](https://streamlit.io/), [Plotly](https://plotly.com/)
- **Backend** : [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Database** : SQLite, [SQLAlchemy](https://www.sqlalchemy.org/)
- **Data Science & ML** : Pandas, Scikit-learn, Transformers (Hugging Face)

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd hr_management_system
```

### 2. Créer un environnement virtuel (recommandé)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances
Assurez-vous d'avoir un fichier `requirements.txt` ou installez les paquets manuellement :
```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l'Application

L'application nécessite que le backend et le frontend tournent simultanément.

### Étape 1 : Démarrer le Backend (API)
Dans un terminal, à la racine du projet :
```bash
uvicorn app.fastapi_app:app --reload
```
- L'API sera accessible sur : `http://localhost:8000`
- Documentation Swagger UI : `http://localhost:8000/docs`

### Étape 2 : Démarrer le Frontend (Streamlit)
Ouvrez un **nouveau terminal**, activez votre environnement virtuel, et lancez :
```bash
streamlit run app/streamlit_app.py
```
- L'interface s'ouvrira automatiquement dans votre navigateur sur : `http://localhost:8501`

## 📂 Structure du Projet

```
hr_management_system/
├── app/
│   ├── fastapi_app.py      # Point d'entrée de l'API Backend
│   └── streamlit_app.py    # Point d'entrée de l'interface Frontend
├── src/
│   ├── backend/
│   │   ├── database.py     # Configuration de la DB
│   │   ├── models.py       # Modèles SQLAlchemy
│   │   ├── crud.py         # Opérations DB
│   │   ├── ml_logic.py     # Logique de prédiction (ML)
│   │   └── migrate_db.py   # Scripts de migration
│   └── frontend/
│       ├── dashboard_view.py    # Vues du tableau de bord
│       ├── add_employee_view.py # Formulaire d'ajout
│       ├── help_view.py         # Page d'aide
│       └── localization.py      # Gestion des traductions
├── data/                   # Stockage de la base de données SQLite
└── README.md               # Documentation du projet
```

## 👥 Auteurs

- **Hippolyte SODJINOU** - Data Scientist / Developer
- **Nercy chancelle Nisabwe** - Data Scientist / Data Analyst
- **Danélius D. ADJENIA** - Data Scientist / Full Stack

## Github repository link:

GitHub: https://github.com/Hippolyte90/Data_Driven_Application_Project#