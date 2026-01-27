import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import sys
import os

# Configuration du chemin pour importer les fonctions du dossier 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.processing import (
    get_company_stats, 
    predict_attrition_risk, 
    calculate_impact, 
    get_age_pyramid_data
)

# Configuration de la page
st.set_page_config(page_title="RH Intelligence Pro", layout="wide")

# Initialisation de la session pour la persistance des données
if "current_employee" not in st.session_state:
    st.session_state.current_employee = None

st.title("📂 Système Expert de Gestion RH")

tab1, tab2 = st.tabs(["👤 Pilotage Profil & Rétention", "🏢 Vue Stratégique Globale"])

# --- ONGLET 1 : PROFIL INDIVIDUEL (LE CŒUR DU CONTRÔLE RH) ---
with tab1:
    st.sidebar.header("🔍 Recherche Employé")
    emp_id = st.sidebar.number_input("ID Employé", min_value=1, value=1028)
    
    if st.sidebar.button("Analyser le profil"):
        try:
            response = requests.get(f"http://127.0.0.1:8000/employee/{emp_id}")
            if response.status_code == 200:
                st.session_state.current_employee = response.json()
            else:
                st.sidebar.error("Employé introuvable.")
        except Exception as e:
            st.sidebar.error("Erreur de connexion API.")

    if st.session_state.current_employee:
        data = st.session_state.current_employee
        risk = predict_attrition_risk(data)
        df_all = get_company_stats()
        
        # 1. TABLEAU DE BORD DU TALENT
        st.header(f"Fiche de Suivi : {data['JobRole']} ({data['Department']})")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Salaire Actuel", f"{data['MonthlyIncome']} $")
        c2.metric("Risque Départ", f"{risk['score']}%", delta_color="inverse")
        c3.metric("Ancienneté", f"{data['TotalWorkingYears']} ans")
        c4.metric("Dernière Promotion", f"{data['YearsSinceLastPromotion']} ans")

        st.markdown("---")

        # 2. ZONE DE SIMULATION (SALAIRE & CONDITIONS)
        col_sim, col_graph = st.columns([1, 2])
        
        with col_sim:
            st.subheader("🧪 Simulateur de Rétention")
            st.write("Testez l'impact des mesures RH :")
            
            # Levier financier
            augm = st.slider("Augmentation de salaire ($)", 0, 3000, 0, step=100)
            
            # Leviers de conditions de travail (Non-financiers)
            st.write("**Conditions de travail :**")
            tele_work = st.checkbox("Accorder du Télétravail (-10% risque)")
            reduce_ot = st.checkbox("Supprimer les Heures Supp (-15% risque)") if data['OverTime'] == 'Yes' else False
            
            # Calcul du risque simulé
            score_actuel = float(risk['score'])
            nouveau_risk = calculate_impact(score_actuel, augm)
            
            if tele_work: nouveau_risk -= 10
            if reduce_ot: nouveau_risk -= 15
            
            score_final = max(0, round(nouveau_risk, 1))
            
            st.metric("Score après mesures", f"{score_final}%", 
                      delta=f"{round(score_final - score_actuel, 1)}%", delta_color="inverse")
            
            if score_final < 30:
                st.success("✅ Risque maîtrisé")
            else:
                st.warning("⚠️ Risque encore élevé : explorez d'autres leviers")

        with col_graph:
            st.subheader("📊 Positionnement Équité Salariale")
            # Graphique montrant l'employé (Point Rouge) par rapport au reste
            fig_pos = px.scatter(df_all, x="Age", y="MonthlyIncome", 
                                 color_discrete_sequence=['#E5E7E9'],
                                 labels={'MonthlyIncome': 'Salaire Mensuel', 'Age': 'Âge'},
                                 title="Salaire vs Âge (L'employé est la cible rouge)")
            
            fig_pos.add_scatter(x=[data['Age']], y=[data['MonthlyIncome']], 
                                mode='markers', marker=dict(size=18, color='#E74C3C', symbol='star'),
                                name="Employé sélectionné")
            st.plotly_chart(fig_pos, use_container_width=True)

        st.markdown("---")
        
        # 3. ANALYSE DU BIEN-ÊTRE (INDIVIDUEL)
        st.subheader("🧠 Analyse du Bien-être et Engagement")
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            # Bar chart des scores de satisfaction
            metrics = {
                "Satisfaction Job": data['JobSatisfaction'],
                "Équilibre Vie Pro": data['WorkLifeBalance'],
                "Environnement": data['EnvironmentSatisfaction'],
                "Relation Manager": data['RelationshipSatisfaction']
            }
            df_m = pd.DataFrame(list(metrics.items()), columns=['Critère', 'Note'])
            fig_metrics = px.bar(df_m, x='Critère', y='Note', range_y=[0,4], 
                                 color='Note', color_continuous_scale='RdYlGn')
            st.plotly_chart(fig_metrics, use_container_width=True)
            
        with col_b2:
            st.info(f"""
            **Diagnostic RH :**
            - **Statut Heures Supp :** {data['OverTime']}
            - **Distance Maison-Travail :** {data['DistanceFromHome']} km
            - **Niveau d'implication :** {data.get('JobInvolvement', 'N/A')}/4
            """)
            with st.expander("Voir toutes les données contractuelles"):
                st.json(data)

# --- ONGLET 2 : ANALYSES GLOBALES (PILOTAGE STRATÉGIQUE) ---
with tab2:
    st.header("🏢 Vue d'Ensemble de l'Entreprise")
    df_global = get_company_stats()
    df_pyr = get_age_pyramid_data()
    
    c_g1, c_g2 = st.columns(2)
    
    with c_g1:
        st.subheader("🔥 Heatmap Satisfaction / Métier")
        fig_h = px.density_heatmap(df_global, x="JobRole", y="JobSatisfaction", 
                                   z="MonthlyIncome", color_continuous_scale="Viridis")
        st.plotly_chart(fig_h, use_container_width=True)
        
    with c_g2:
        st.subheader("👥 Pyramide des Âges")
        fig_p = px.bar(df_pyr, x="Effectif", y="Tranche_Age", color="Gender", orientation='h')
        st.plotly_chart(fig_p, use_container_width=True)

    st.markdown("---")
    st.subheader("🎯 Matrice de Performance vs Implication")
    fig_9 = px.scatter(df_global, x="JobSatisfaction", y="WorkLifeBalance", 
                       size="MonthlyIncome", color="Department", hover_data=['JobRole'])
    fig_9.add_hline(y=2.5, line_dash="dot")
    fig_9.add_vline(x=2.5, line_dash="dot")
    st.plotly_chart(fig_9, use_container_width=True)