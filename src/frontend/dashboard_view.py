import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px


API_URL = os.getenv("API_URL", "http://localhost:8000")

# Set the CSS styles for KPI cards
st.markdown("""
<style>
.kpi-card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}
.kpi-title {
    font-size: 14px;
    color: #6b7280;
}
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    margin-top: 8px;
}
.green { color: #16a34a; }
.red { color: #dc2626; }
.blue { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

def card_container():
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)

def end_card():
    st.markdown('</div>', unsafe_allow_html=True)

def render_search_view():
    """Renders the isolated search result view with evaluation and comment actions."""
    emp_id = st.session_state.search_emp_id
    
    # Styles specific to the employee card
    st.markdown("""
    <style>
    .employee-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 30px;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .employee-header {
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 20px;
        text-align: center;
        border-bottom: 2px solid rgba(255,255,255,0.3);
        padding-bottom: 15px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
    }
    .info-item {
        background: rgba(255,255,255,0.15);
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    .info-label {
        font-size: 12px;
        text-transform: uppercase;
        opacity: 0.8;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    .info-value {
        font-size: 20px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🔍 Résultat de la recherche")

    try:
        res = requests.get(f"{API_URL}/employee/{emp_id}", timeout=5)
    except Exception as e:
        st.error(f"Erreur réseau: {e}")
        if st.button("🏠 Retour à l'accueil"):
            del st.session_state.search_emp_id
            st.rerun()
        return

    if res.status_code == 404:
        st.warning(f"⚠️ Aucun employé trouvé avec l'ID **{emp_id}**. Veuillez essayer un autre ID via la barre latérale.")
        if st.button("🏠 Retour à l'accueil"):
            del st.session_state.search_emp_id
            st.rerun()
        return
    
    if res.status_code != 200:
        st.error(f"Erreur lors de la récupération des données (Code {res.status_code}).")
        if st.button("🏠 Retour à l'accueil"):
            del st.session_state.search_emp_id
            st.rerun()
        return

    emp = res.json()

    # Employee Card Display
    st.markdown(f"""
    <div class="employee-card">
        <div class="employee-header">
            👤 Employé #{emp_id}
        </div>
        <div class="info-grid">
            <div class="info-item"><div class="info-label">🏢 Département</div><div class="info-value">{emp.get('Department', 'N/A')}</div></div>
            <div class="info-item"><div class="info-label">💰 Salaire Mensuel</div><div class="info-value">{emp.get('MonthlyIncome', 0):,}€</div></div>
            <div class="info-item"><div class="info-label">📅 Années (Cie)</div><div class="info-value">{emp.get('YearsAtCompany', 0)} ans</div></div>
            <div class="info-item"><div class="info-label">🎯 Poste</div><div class="info-value">{emp.get('JobRole', 'N/A')}</div></div>
            <div class="info-item"><div class="info-label">😊 Satisfaction Job</div><div class="info-value">{emp.get('JobSatisfaction', 'N/A')}/4</div></div>
            <div class="info-item"><div class="info-label">🧠 Implication</div><div class="info-value">{emp.get('JobInvolvement', 'N/A')}/4</div></div>
            <div class="info-item"><div class="info-label">🌍 Env. Satisfaction</div><div class="info-value">{emp.get('EnvironmentSatisfaction', 'N/A')}/4</div></div>
            <div class="info-item"><div class="info-label">⚖️ Work-Life Balance</div><div class="info-value">{emp.get('WorkLifeBalance', 'N/A')}/4</div></div>
            <div class="info-item"><div class="info-label">🚪 Attrition</div><div class="info-value" style="color: {'#ff6b6b' if emp.get('Attrition') == 'Yes' else 'white'}; font-weight:bold;">{emp.get('Attrition', 'N/A')}</div></div>
            <div class="info-item"><div class="info-label">⭐ Note d'évaluation</div><div class="info-value">{emp.get('evaluation_note', 'N/A') if emp.get('evaluation_note') is not None else 'N/A'}</div></div>
            <div class="info-item"><div class="info-label">💬 Commentaire</div><div class="info-value">{emp.get('comment', 'No') if emp.get('comment') is not None else 'No'}</div></div>

        </div>
    </div>
    """, unsafe_allow_html=True)

    # Evaluation & Comment Form
    st.subheader("📝 Évaluation et Commentaire")
    st.info("Analysez les informations ci-dessus, puis ajoutez ou modifiez la note et le commentaire si nécessaire.")

    with st.form("eval_comment_form"):
        c1, c2 = st.columns(2)
        with c1:
            current_note = emp.get('evaluation_note')
            val_note = float(current_note) if current_note is not None else 5.0
            new_note = st.slider("⭐ Note d'évaluation (/10)", 0.0, 10.0, val_note, 0.1)
        with c2:
            current_comment = emp.get('comment', '')
            new_comment = st.text_area("💬 Commentaire", value=current_comment if current_comment else "", height=100)
        
        if st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True):
            try:
                requests.post(f"{API_URL}/update_evaluation_note", json={"id": emp_id, "evaluation_note": new_note}, timeout=5)
                requests.post(f"{API_URL}/update_comment", json={"id": emp_id, "comment": new_comment}, timeout=5)
                st.success("Informations enregistrées avec succès !")
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de l'enregistrement: {e}")

    st.markdown("---")
    if st.button("🏠 Retour à l'accueil", use_container_width=True):
        del st.session_state.search_emp_id
        st.rerun()

def render_dashboard():
    """Renders the main dashboard view with KPIs and visualizations."""
    
    # If a search is active, show ONLY the search view
    if "search_emp_id" in st.session_state:
        render_search_view()
        return
    
    st.title("🟩 Performance Hub")
    # Header & KPI
    try:
        stats = requests.get(f"{API_URL}/stats", timeout=5).json()
    except Exception as e:
        st.error(f"Unable to retrieve statistics: {e}")
        return

    c1, c2, c3 = st.columns(3)
    #c1.metric("Total Employés", stats.get('total', 0))
#     c1.metric( "👥 Total Employés", f"{stats.get('total', 0):,}")
#     c2.metric(
#     "📉 Taux d’Attrition",
#     f"{stats.get('attrition', 0):.1f} %"
# )
#     #c2.metric("Taux Attrition", stats.get('attrition', 'N/A'))

#     c3.metric("Satisfaction Moyenne", stats.get('satisfaction', 'N/A'))
    with c1:
        st.markdown(
                        f"""
                        <div style="background-color:#009fe3;padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>👥 Total Employees</h3><span style="font-size:40px;">{stats.get('total', 0):,}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    
    with c2:
        attr_str = stats.get('attrition', '0')
        attr = float(str(attr_str).rstrip('%'))
        if attr > 15:
            color = "red"
        elif attr > 10 and attr <= 15:
            color = "orange"
        else:
            color = "green"
                
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>📉 Attrition Rate</h3><span style="font-size:40px;">{attr:.1f}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
    
    with c3:
        sat_str = stats.get('satisfaction', '0')
        sat = float(str(sat_str).rstrip('/4').strip())
        if sat < 2:
            color = "red"
        elif sat < 3 and sat > 2:
            color = "orange"
        else:
            color = "green"
        
        
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>😊 Average Satisfaction</h3><span style="font-size:40px;">{sat:.1f} / 4</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
 
    st.divider()


    # Performance by Department
    
    cl1, cl2 = st.columns(2, gap="large")
    with cl1:
        st.subheader("Performance by Department")
        try:
            res = requests.get(f"{API_URL}/employee", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
    
        if res.status_code == 200:
            emp = res.json()
            data_df = pd.DataFrame(emp)
            
        def plot_performance_by_department(df: pd.DataFrame):
            """
            Plots the average performance rating by department as a bar chart.
            """
            # Select required columns
            subset = df[['Department', 'PerformanceRating']]
            
            # Group by department and compute mean performance rating
            grouped = (
                subset
                .groupby('Department', as_index=False)
                .agg(AveragePerformance=('PerformanceRating', 'mean'))
                .sort_values('AveragePerformance', ascending=False)
            )
            
            # Create interactive bar chart
            fig = px.bar(
                grouped,
                x='Department',
                y='AveragePerformance',
                text=grouped['AveragePerformance'].round(2),
                template='plotly_white'
            )
            
            # Improve layout and readability
            fig.update_layout(
                yaxis=dict(
                    title='Average Performance Rating',
                    range=[0, 8],          # Logical scale
                    tickmode='linear',
                    tick0=0,
                    dtick=0.5
                )
            )
            
            fig.update_traces(
                textposition='outside',
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Average Rating: %{y:.2f}/4<extra></extra>"
                )
            )
            
            # Display in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
        card_container()            
        plot_performance_by_department(data_df)
        end_card()
        
    with cl2:
        st.subheader("Work-Life Balance Distribution by Department")
        def display_wlb_by_department(df):
            """
            Groups the data and displays a 100% stacked bar chart 
            showing Work-Life Balance levels across all departments.
            """
            
            # 1. Create a local copy to avoid modifying the original dataframe
            df_plot = df.copy()

            # 2. Mapping numerical values to English labels
            # Based on: 1 'Bad', 2 'Good', 3 'Better', 4 'Best'
            wlb_mapping = {
                1: '1-Bad',
                2: '2-Good',
                3: '3-Better',
                4: '4-Best'
            }
            df_plot['WLB_Status'] = df_plot['WorkLifeBalance'].map(wlb_mapping)

            # 3. Create the stacked bar chart
            # 'barnorm=percent' automatically handles the grouping and percentage calculation
            fig = px.histogram(
                df_plot, 
                x="Department", 
                color="WLB_Status",
                category_orders={"WLB_Status": ["1-Bad", "2-Good", "3-Better", "4-Best"]},
                barnorm='percent', 
                text_auto='.1f',   # Shows the percentage label on each bar
                color_discrete_map={
                    "1-Bad": "#FF4B4B",    # Red for alert
                    "2-Good": "#FFAA00",   # Orange
                    "3-Better": "#00CC96", # Green
                    "4-Best": "#0068C9"    # Blue
                }
            )

            # 4. Styling the layout for an HR-friendly look
            fig.update_layout(
                yaxis_title="Percentage of Employees (%)",
                xaxis_title="Department",
                legend_title="WLB Rating",
                template="plotly_white",
                uniformtext_minsize=8, 
                uniformtext_mode='hide'
            )

            # 5. Render in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
        card_container()            
        display_wlb_by_department(data_df)
        end_card()
            
    st.divider()
    
    
    
                    


# Columns order for department data display
useful_cols = ['id','Age', 
                'Education', 'JobRole', 
                'MonthlyIncome', 'EnvironmentSatisfaction',
                'JobInvolvement', 'RelationshipSatisfaction', 
                'PerformanceRating', 'JobSatisfaction','WorkLifeBalance','Attrition'] 


# Sale department data view
def render_sales_data():
    """Renders the Sales department dashboard view with KPIs and visualizations."""
    
    st.title("🟩 Performance Hub")
    # Header & KPI
    try:
        sales_stats = requests.get(f"{API_URL}/sales/sales_stats", timeout=5).json()
    except Exception as e:
        st.error(f"Unable to retrieve statistics: {e}")
        return

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
                        f"""
                        <div style="background-color:#009fe3;padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>👥 Total Employees</h3><span style="font-size:40px;">{sales_stats.get('total_employees', 0):,}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    
    with c2:
        attr_str = sales_stats.get('attrition_rate', '0')
        attr = float(str(attr_str).rstrip('%'))
        if attr > 15:
            color = "red"
        elif attr > 10 and attr <= 15:
            color = "orange"
        else:
            color = "green"
                
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>📉 Attrition Rate</h3><span style="font-size:40px;">{attr:.1f}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
    
    with c3:
        sat_str = sales_stats.get('average_job_satisfaction', '0')
        sat = float(str(sat_str).rstrip('/4').strip())
        if sat < 2:
            color = "red"
        elif sat < 3 and sat > 2:
            color = "orange"
        else:
            color = "green"
        
        
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>😊 Average Satisfaction</h3><span style="font-size:40px;">{sat:.1f} / 4</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
 
    st.divider()

    
    cl1, cl2 = st.columns(2, gap="large")
    
    # Attrition Rate (%) by Job Role
    with cl1:
        st.subheader("Attrition Rate (%) by Job Role")
        try:
            res = requests.get(f"{API_URL}/sales", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
    
        if res.status_code == 200:
            emp = res.json()
            data_df = pd.DataFrame(emp)
            
        def display_attrition_by_role(df: pd.DataFrame):
            """
            Calculates the attrition rate per job role and displays 
            a sorted horizontal bar chart.
            """
            # 1. Prepare data: Convert 'Yes'/'No' to 1/0 to calculate the mean (rate)
            df_temp = df.copy()
            df_temp['Attrition_Numeric'] = df_temp['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
            
            # 2. Group by Job Role and calculate the average
            attrition_data = df_temp.groupby('JobRole')['Attrition_Numeric'].mean().reset_index()
            attrition_data['Attrition_Rate'] = attrition_data['Attrition_Numeric'] * 100
            
            # 3. Sort for better visualization
            attrition_data = attrition_data.sort_values(by='Attrition_Rate', ascending=True)

            # 4. Create the Plotly Horizontal Bar Chart
            fig = px.bar(
                attrition_data,
                x='Attrition_Rate',
                y='JobRole',
                orientation='h',
                text_auto='.1f',
                color='Attrition_Rate',
                color_continuous_scale='Reds' # Darker red for higher attrition roles
            )

            # 5. UI Layout adjustments
            fig.update_layout(
                xaxis_title="Attrition Rate (Percentage)",
                yaxis_title="Position / Job Role",
                showlegend=False,
                template="plotly_white",
                margin=dict(l=20, r=20, t=40, b=20)
            )

            # 6. Render in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        card_container()            
        display_attrition_by_role(data_df)
        end_card()
        
        
    with cl2:
        st.subheader("Job Satisfaction Distribution by Role")
        def display_satisfaction_by_role(df):
            """
            Groups the data by Job Role and Job Satisfaction levels,
            displaying a 100% stacked bar chart.
            """
            
            # 1. Create a copy and map numerical values to English labels
            # Based on your mapping: 1 'Low', 2 'Medium', 3 'High', 4 'Very High'
            df_plot = df.copy()
            satisfaction_mapping = {
                1: '1-Low',
                2: '2-Medium',
                3: '3-High',
                4: '4-Very High'
            }
            df_plot['Satisfaction_Level'] = df_plot['JobSatisfaction'].map(satisfaction_mapping)

            # 2. Create the 100% stacked bar chart
            # 'barnorm=percent' handles the distribution calculation automatically
            fig = px.histogram(
                df_plot, 
                y="JobRole", 
                color="Satisfaction_Level",
                category_orders={"Satisfaction_Level": ["1-Low", "2-Medium", "3-High", "4-Very High"]},
                barnorm='percent', 
                text_auto='.1f',
                orientation='h', # Horizontal for easier reading of role names
                color_discrete_map={
                    "1-Low": "#E74C3C",        # Red
                    "2-Medium": "#F39C12",     # Orange
                    "3-High": "#3498DB",       # Blue
                    "4-Very High": "#27AE60"   # Green
                }
            )

            # 3. Styling the layout
            fig.update_layout(
                xaxis_title="Percentage of Employees (%)",
                yaxis_title="Job Role",
                legend_title="Satisfaction Level",
                template="plotly_white",
                margin=dict(l=20, r=20, t=50, b=20)
            )

            # 4. Display in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        
        card_container()            
        display_satisfaction_by_role(data_df)
        end_card()
            

    st.divider()
    
    
    st.subheader("Sales Department data")
    
    response = requests.get(f"{API_URL}/sales", timeout=5)

    if response.status_code == 200:
        sales_data = response.json()
    else:
        st.error("Unable to retrieve Sales data.")
        st.stop()
     
    df_sales = pd.DataFrame(sales_data)
    df_sales = df_sales[useful_cols]
    
    st.dataframe(df_sales, use_container_width=True, hide_index=True)
    
    
# RD department data view
def render_rd_data():
    """Renders the R&D department dashboard view with KPIs and visualizations."""
    
    st.title("🟩 Talent Performance Hub")
    # Header & KPI
    try:
        rd_stats = requests.get(f"{API_URL}/rd/rd_stats", timeout=5).json()
    except Exception as e:
        st.error(f"Unable to retrieve statistics: {e}")
        return

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(
                        f"""
                        <div style="background-color:#009fe3;padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>👥 Total Employees</h3><span style="font-size:40px;">{rd_stats.get('total_employees', 0):,}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    
    
    with c2:
        attr_str = rd_stats.get('attrition_rate', '0')
        attr = float(str(attr_str).rstrip('%'))

        if attr > 15:
            color = "red"
        elif attr > 10 and attr <= 15:
            color = "orange"
        else:
            color = "green"
                
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>📉 Attrition Rate</h3><span style="font-size:40px;">{attr:.1f}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
    
    with c3:
        sat_str = rd_stats.get('average_job_satisfaction', '0')
        sat = float(str(sat_str).rstrip('/4').strip())
        if sat < 2:
            color = "red"
        elif sat < 3 and sat > 2:
            color = "orange"
        else:
            color = "green"
        
        
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>😊 Average Satisfaction</h3><span style="font-size:40px;">{sat:.1f} / 4</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
 
    st.divider()
    
    cl1, cl2 = st.columns(2, gap="large")
    
    # Attrition Rate (%) by Job Role
    with cl1:
        st.subheader("Attrition Rate (%) by Job Role")
        try:
            res = requests.get(f"{API_URL}/rd", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
    
        if res.status_code == 200:
            emp = res.json()
            data_df = pd.DataFrame(emp)
            
        def display_attrition_by_role(df: pd.DataFrame):
            """
            Calculates the attrition rate per job role and displays 
            a sorted horizontal bar chart.
            """
            # 1. Prepare data: Convert 'Yes'/'No' to 1/0 to calculate the mean (rate)
            df_temp = df.copy()
            df_temp['Attrition_Numeric'] = df_temp['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
            
            # 2. Group by Job Role and calculate the average
            attrition_data = df_temp.groupby('JobRole')['Attrition_Numeric'].mean().reset_index()
            attrition_data['Attrition_Rate'] = attrition_data['Attrition_Numeric'] * 100
            
            # 3. Sort for better visualization
            attrition_data = attrition_data.sort_values(by='Attrition_Rate', ascending=True)

            # 4. Create the Plotly Horizontal Bar Chart
            fig = px.bar(
                attrition_data,
                x='Attrition_Rate',
                y='JobRole',
                orientation='h',
                text_auto='.1f',
                color='Attrition_Rate',
                color_continuous_scale='Reds' # Darker red for higher attrition roles
            )

            # 5. UI Layout adjustments
            fig.update_layout(
                xaxis_title="Attrition Rate (Percentage)",
                yaxis_title="Position / Job Role",
                showlegend=False,
                template="plotly_white",
                margin=dict(l=20, r=20, t=40, b=20)
            )

            # 6. Render in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        card_container()            
        display_attrition_by_role(data_df)
        end_card()
        
        
    with cl2:
        st.subheader("Job Satisfaction Distribution by Role")
        def display_satisfaction_by_role(df):
            """
            Groups the data by Job Role and Job Satisfaction levels,
            displaying a 100% stacked bar chart.
            """
            
            # 1. Create a copy and map numerical values to English labels
            # Based on your mapping: 1 'Low', 2 'Medium', 3 'High', 4 'Very High'
            df_plot = df.copy()
            satisfaction_mapping = {
                1: '1-Low',
                2: '2-Medium',
                3: '3-High',
                4: '4-Very High'
            }
            df_plot['Satisfaction_Level'] = df_plot['JobSatisfaction'].map(satisfaction_mapping)

            # 2. Create the 100% stacked bar chart
            # 'barnorm=percent' handles the distribution calculation automatically
            fig = px.histogram(
                df_plot, 
                y="JobRole", 
                color="Satisfaction_Level",
                category_orders={"Satisfaction_Level": ["1-Low", "2-Medium", "3-High", "4-Very High"]},
                barnorm='percent', 
                text_auto='.1f',
                orientation='h', # Horizontal for easier reading of role names
                color_discrete_map={
                    "1-Low": "#E74C3C",        # Red
                    "2-Medium": "#F39C12",     # Orange
                    "3-High": "#3498DB",       # Blue
                    "4-Very High": "#27AE60"   # Green
                }
            )

            # 3. Styling the layout
            fig.update_layout(
                xaxis_title="Percentage of Employees (%)",
                yaxis_title="Job Role",
                legend_title="Satisfaction Level",
                template="plotly_white",
                margin=dict(l=20, r=20, t=50, b=20)
            )

            # 4. Display in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        
        card_container()            
        display_satisfaction_by_role(data_df)
        end_card()
            
    st.divider()
    

    # RD department data display
    st.subheader("Research & Development Department data")
    
    response = requests.get(f"{API_URL}/rd", timeout=5)

    if response.status_code == 200:
        rd_data = response.json()
    else:
        st.error("Unable to retrieve R&D data.")
        st.stop()
     
    df_rd = pd.DataFrame(rd_data)
    df_rd = df_rd[useful_cols]
    
    st.dataframe(df_rd, use_container_width=True, hide_index=True)
    
# HR department data view
def render_hr_data():
    """Renders the HR department dashboard view with KPIs and visualizations."""
    
    st.title("🟩 Talent Performance Hub")
    # Header & KPI
    try:
        hr_stats = requests.get(f"{API_URL}/hr/hr_stats", timeout=5).json()
    except Exception as e:
        st.error(f"Unable to retrieve statistics: {e}")
        return  
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
                        f"""
                        <div style="background-color:#009fe3;padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>👥 Total Employees</h3><span style="font-size:40px;">{hr_stats.get('total_employees', 0):,}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )   
    with c2:
        attr_str = hr_stats.get('attrition_rate', '0')
        attr = float(str(attr_str).rstrip('%'))
        if attr > 15:
            color = "red"
        elif attr > 10 and attr <= 15:
            color = "orange"
        else:
            color = "green"        
               
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>📉 Attrition Rate</h3><span style="font-size:40px;">{attr:.1f}%</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    with c3:
        sat_str = hr_stats.get('average_job_satisfaction', '0')
        sat = float(str(sat_str).rstrip('/4').strip())
        if sat < 2:
            color = "red"
        elif sat < 3 and sat > 2:
            color = "orange"
        else:
            color = "green"        
        st.markdown(
                        f"""
                        <div style="background-color:{color};padding:10px;
                        border-radius:8px;text-align:center;color:white;
                        font-weight:bold;height:130px; display:flex;
                        flex-direction:column;justify-content:center; align-items:center;">
                        <h3>😊 Average Satisfaction</h3><span style="font-size:40px;">{sat:.1f} / 4</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        
    st.divider()
        
    cl1, cl2 = st.columns(2, gap="large")
    
    # Attrition Rate (%) by Job Role
    with cl1:
        st.subheader("Attrition Rate (%) by Job Role")
        try:
            res = requests.get(f"{API_URL}/hr", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
    
        if res.status_code == 200:
            emp = res.json()
            data_df = pd.DataFrame(emp)
            
        def display_attrition_by_role(df: pd.DataFrame):
            """
            Calculates the attrition rate per job role and displays 
            a sorted horizontal bar chart.
            """
            # 1. Prepare data: Convert 'Yes'/'No' to 1/0 to calculate the mean (rate)
            df_temp = df.copy()
            df_temp['Attrition_Numeric'] = df_temp['Attrition'].apply(lambda x: 1 if x == 'Yes' else 0)
            
            # 2. Group by Job Role and calculate the average
            attrition_data = df_temp.groupby('JobRole')['Attrition_Numeric'].mean().reset_index()
            attrition_data['Attrition_Rate'] = attrition_data['Attrition_Numeric'] * 100
            
            # 3. Sort for better visualization
            attrition_data = attrition_data.sort_values(by='Attrition_Rate', ascending=True)

            # 4. Create the Plotly Horizontal Bar Chart
            fig = px.bar(
                attrition_data,
                x='Attrition_Rate',
                y='JobRole',
                orientation='h',
                text_auto='.1f',
                color='Attrition_Rate',
                color_continuous_scale='Reds' # Darker red for higher attrition roles
            )

            # 5. UI Layout adjustments
            fig.update_layout(
                xaxis_title="Attrition Rate (Percentage)",
                yaxis_title="Position / Job Role",
                showlegend=False,
                template="plotly_white",
                margin=dict(l=20, r=20, t=40, b=20)
            )

            # 6. Render in Streamlit
            st.plotly_chart(fig, use_container_width=True)

        card_container()            
        display_attrition_by_role(data_df)
        end_card()
        
        
    with cl2:
        st.subheader("Job Satisfaction Distribution by Role")
        def display_satisfaction_by_role(df):
            """
            Groups the data by Job Role and Job Satisfaction levels,
            displaying a 100% stacked bar chart.
            """
            
            # 1. Create a copy and map numerical values to English labels
            # Based on your mapping: 1 'Low', 2 'Medium', 3 'High', 4 'Very High'
            df_plot = df.copy()
            satisfaction_mapping = {
                1: '1-Low',
                2: '2-Medium',
                3: '3-High',
                4: '4-Very High'
            }
            df_plot['Satisfaction_Level'] = df_plot['JobSatisfaction'].map(satisfaction_mapping)

            # 2. Create the 100% stacked bar chart
            # 'barnorm=percent' handles the distribution calculation automatically
            fig = px.histogram(
                df_plot, 
                y="JobRole", 
                color="Satisfaction_Level",
                category_orders={"Satisfaction_Level": ["1-Low", "2-Medium", "3-High", "4-Very High"]},
                barnorm='percent', 
                text_auto='.1f',
                orientation='h', # Horizontal for easier reading of role names
                color_discrete_map={
                    "1-Low": "#E74C3C",        # Red
                    "2-Medium": "#F39C12",     # Orange
                    "3-High": "#3498DB",       # Blue
                    "4-Very High": "#27AE60"   # Green
                }
            )

            # 3. Styling the layout
            fig.update_layout(
                xaxis_title="Percentage of Employees (%)",
                yaxis_title="Job Role",
                legend_title="Satisfaction Level",
                template="plotly_white",
                margin=dict(l=20, r=20, t=50, b=20)
            )

            # 4. Display in Streamlit
            st.plotly_chart(fig, use_container_width=True)
        
        card_container()            
        display_satisfaction_by_role(data_df)
        end_card()
            
    st.divider()
    st.subheader("Human Resources Department data") 
    response = requests.get(f"{API_URL}/hr", timeout=5)
    if response.status_code == 200:
        hr_data = response.json()
    else:
        st.error("Unable to retrieve HR data.")
        st.stop()
    df_hr = pd.DataFrame(hr_data)
    df_hr = df_hr[useful_cols]
    
    st.dataframe(df_hr, use_container_width=True, hide_index=True)
    
    

    