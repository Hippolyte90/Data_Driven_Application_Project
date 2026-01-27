import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="PerformTrack RH", layout="wide")

st.title("🚀 PerformTrack - Évaluation RH")

# --- Système d'identification (Traçabilité) ---
if 'agent_id' not in st.session_state:
    st.subheader("Connexion Agent RH")
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        # Appel à l'API FastAPI pour vérifier l'identité
        response = requests.post("http://127.0.0.1:8000/login", 
                                 json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            st.session_state.agent_id = data['user_id']
            st.session_state.agent_name = data['full_name']
            st.rerun()
        else:
            st.error("Identifiants incorrects")
else:
    st.sidebar.success(f"Connecté : {st.session_state.agent_name}")
    if st.sidebar.button("Déconnexion"):
        del st.session_state.agent_id
        st.rerun()

    # --- Affichage des données IBM ---
    st.header("Tableau de bord de performance")
    
    # Récupération des employés via l'API
    resp = requests.get("http://127.0.0.1:8000/employees")
    if resp.status_code == 200:
        df = pd.DataFrame(resp.json())
        st.dataframe(df, use_container_width=True)
        
        # Exemple de graphique simple
        st.bar_chart(df.set_index('JobRole')['PerformanceRating'])
    else:
        st.error("Impossible de charger les données")