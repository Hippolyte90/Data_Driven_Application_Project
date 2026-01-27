import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

def render_add_employee():
    st.title("➕ Enregistrer un nouvel employé")

    with st.form("add_employee_form"):
        col_1, col_2 = st.columns(2)
        
        with col_1:
            auto_id = st.checkbox("Générer l'identifiant automatiquement", value=True)
            manual_id = st.number_input("ID Manuel (si non automatique)", min_value=1, step=1)
            age = st.number_input("Age", min_value=18, max_value=70, value=30)
            dept = st.selectbox("Département", ["Sales", "Research & Development", "Human Resources"])
            
        with col_2:
            income = st.number_input("Salaire Mensuel (€)", min_value=0, value=2500)
            years = st.number_input("Années dans l'entreprise", min_value=0, value=0)
            satisfaction = st.slider("Niveau de satisfaction initial", 1, 4, 3)

        submitted = st.form_submit_button("Enregistrer l'employé")
        
        if submitted:
            payload = {
                "auto_id": auto_id,
                "id": manual_id,
                "Age": age,
                "Department": dept,
                "MonthlyIncome": income,
                "YearsAtCompany": years,
                "JobSatisfaction": satisfaction
            }
            try:
                response = requests.post(f"{API_URL}/add_employee", json=payload, timeout=10)
            except Exception as e:
                st.error(f"Erreur réseau: {e}")
            else:
                if response.status_code == 200:
                    new_id_created = response.json().get("id")
                    st.success(f"Employé enregistré avec succès ! ID attribué : {new_id_created}")
                else:
                    try:
                        error_detail = response.json().get("detail", response.text)
                    except Exception:
                        error_detail = response.text
                    st.error(f"Erreur : {error_detail}")
