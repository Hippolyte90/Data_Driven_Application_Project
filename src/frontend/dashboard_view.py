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


def render_dashboard():
    st.title("🟩 HR Dashboard")
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
    
    cl1, cl2 = st.columns(2)
    with cl1:
        st.subheader("Performance by Department")
        try:
            res = requests.get(f"{API_URL}/employee", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
    
        if res.status_code == 200:
            emp = res.json()
            data_df = pd.DataFrame(emp)
            
        def plot_performance_by_department(df):
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
                title='Average Performance Rating by Department',
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
        st.subheader("Sales Distribution by Job Role")
    
    
    st.divider()
    
    
    
    # Search employee
    st.subheader("Search for an employee by ID")
    emp_id = st.number_input("Enter the employee ID", min_value=1, step=1)
    if st.button("Search"):
        try:
            res = requests.get(f"{API_URL}/employee/{emp_id}", timeout=5)
        except Exception as e:
            st.error(f"Network error: {e}")
            return
        if res.status_code == 200:
            emp = res.json()
            st.write(f"### Information for employee: {emp_id}")
            col_a, col_b = st.columns(2)
            col_a.write(f"**Department:** {emp.get('Department')}")
            col_a.write(f"**Monthly Salary:** {emp.get('MonthlyIncome')}€")
            col_b.write(f"**Years in the company:** {emp.get('YearsAtCompany')}")
            col_b.write(f"**Current Score:** {emp.get('score')}%")

            # Score
            new_score = st.slider("Assign a new score (%)", 0, 100, int(emp.get('score', 0)))
            if st.button("Save the score"):
                try:
                    requests.post(f"{API_URL}/update_score", json={"id": emp_id, "score": new_score}, timeout=5)
                    st.success("Score mis à jour !")
                except Exception as e:
                    st.error(f"Error during update: {e}")

            # Prédiction Attrition
            st.divider()
            st.subheader("Future simulation")
            add_years = st.number_input("Années supplémentaires", 0, 20, 0)
            add_salary = st.number_input("Augmentation de salaire prévue", 0, 5000, 0)
            if st.button("Prédire Attrition"):
                risk = "Elevé" if (emp.get('JobSatisfaction', 3) < 2 and add_salary < 500) else "Faible"
                st.warning(f"Risque d'attrition estimé : {risk}")
        else:
            st.error("Employé introuvable.")


# Columns order for department data display
useful_cols = ['id','Age', 
                'Education', 'JobRole', 
                'MonthlyIncome', 'EnvironmentSatisfaction',
                'JobInvolvement', 'RelationshipSatisfaction', 
                'PerformanceRating', 'JobSatisfaction','WorkLifeBalance','Attrition'] 


# Sale department data view
def render_sales_data():
    st.title("🟩 HR Dashboard")
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

    # Search employee
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
    st.title("🟩 HR Dashboard")
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

    # Search employee
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
    st.title("🟩 HR Dashboard")
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
    
    

    