"""
View module for adding new employees.
Provides a form to input employee data and sends it to the backend.
"""
import os
import streamlit as st
import requests
import pandas as pd

API_URL = os.getenv("API_URL", "http://localhost:8000")

def render_add_employee():
    """
    Renders the Add Employee view with a comprehensive form covering all data points.
    Maintains a session-based list of added employees for verification.
    """
    st.title("➕ Register New Employee")
    st.markdown("Enter all employee details below. Default values are provided for ease of use.")

    # Initialize session state for added employees if not present
    if "added_employees_list" not in st.session_state:
        st.session_state.added_employees_list = []

    with st.form("add_employee_form"):
        st.subheader("1. Identification & Personal Details")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            auto_id = st.checkbox("Auto-generate ID", value=True)
            manual_id = st.number_input("Manual ID", min_value=1, step=1, disabled=auto_id)
            age = st.number_input("Age", min_value=18, max_value=80, value=30)
            gender = st.selectbox("Gender", ["Male", "Female"])
            
        with col2:
            marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
            education = st.selectbox("Education Level", [1, 2, 3, 4, 5], help="1: Below College, 2: College, 3: Bachelor, 4: Master, 5: Doctor")
            education_field = st.selectbox("Education Field", ["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])
            
        with col3:
            distance = st.number_input("Distance From Home (km)", min_value=0, value=5)
            
        st.markdown("---")
        st.subheader("2. Job & Department Info")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            dept = st.selectbox("Department", ["Sales", "Research & Development", "Human Resources"])
            role = st.selectbox("Job Role", [
                "Sales Executive", "Research Scientist", "Laboratory Technician", 
                "Manufacturing Director", "Healthcare Representative", "Manager", 
                "Sales Representative", "Research Director", "Human Resources"
            ])
            job_level = st.selectbox("Job Level", [1, 2, 3, 4, 5])

        with col5:
            business_travel = st.selectbox("Business Travel", ["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
            overtime = st.selectbox("OverTime", ["No", "Yes"])
            standard_hours = st.number_input("Standard Hours", value=80, disabled=True)

        with col6:
            attrition = st.selectbox("Attrition (Current Status)", ["No", "Yes"], index=0, help="Usually 'No' for new hires.")

        st.markdown("---")
        st.subheader("3. Compensation")
        col7, col8, col9 = st.columns(3)
        
        with col7:
            monthly_income = st.number_input("Monthly Income", min_value=0, value=3000)
            daily_rate = st.number_input("Daily Rate", min_value=0, value=500)
            hourly_rate = st.number_input("Hourly Rate", min_value=0, value=50)
            
        with col8:
            monthly_rate = st.number_input("Monthly Rate", min_value=0, value=10000)
            percent_hike = st.number_input("Percent Salary Hike", min_value=0, value=10)
            stock_level = st.selectbox("Stock Option Level", [0, 1, 2, 3])
            
        with col9:
            pass # Spacer

        st.markdown("---")
        st.subheader("4. History & Tenure")
        col10, col11, col12 = st.columns(3)
        
        with col10:
            num_companies = st.number_input("Num Companies Worked", min_value=0, value=1)
            total_working_years = st.number_input("Total Working Years", min_value=0, value=5)
            training_times = st.number_input("Training Times Last Year", min_value=0, value=2)
            
        with col11:
            years_at_company = st.number_input("Years At Company", min_value=0, value=0)
            years_in_role = st.number_input("Years In Current Role", min_value=0, value=0)
            
        with col12:
            years_since_promotion = st.number_input("Years Since Last Promotion", min_value=0, value=0)
            years_with_manager = st.number_input("Years With Curr Manager", min_value=0, value=0)

        st.markdown("---")
        st.subheader("5. Satisfaction & Performance Ratings (1-4)")
        col13, col14, col15 = st.columns(3)
        
        with col13:
            env_sat = st.slider("Environment Satisfaction", 1, 4, 3)
            job_sat = st.slider("Job Satisfaction", 1, 4, 3)
            
        with col14:
            rel_sat = st.slider("Relationship Satisfaction", 1, 4, 3)
            work_life = st.slider("Work Life Balance", 1, 4, 3)
            
        with col15:
            job_inv = st.slider("Job Involvement", 1, 4, 3)
            perf_rating = st.slider("Performance Rating", 1, 4, 3)

        submitted = st.form_submit_button("💾 Register Employee", use_container_width=True)
        
        if submitted:
            # Construct payload with all fields matching the Employee model
            payload = {
                "auto_id": auto_id,
                "id": manual_id if not auto_id else 0,
                "Age": age,
                "Attrition": attrition,
                "BusinessTravel": business_travel,
                "DailyRate": daily_rate,
                "Department": dept,
                "DistanceFromHome": distance,
                "Education": education,
                "EducationField": education_field,
                "EnvironmentSatisfaction": env_sat,
                "Gender": gender,
                "HourlyRate": hourly_rate,
                "JobInvolvement": job_inv,
                "JobLevel": job_level,
                "JobRole": role,
                "JobSatisfaction": job_sat,
                "MaritalStatus": marital_status,
                "MonthlyIncome": monthly_income,
                "MonthlyRate": monthly_rate,
                "NumCompaniesWorked": num_companies,
                "OverTime": overtime,
                "PercentSalaryHike": percent_hike,
                "PerformanceRating": perf_rating,
                "RelationshipSatisfaction": rel_sat,
                "StandardHours": standard_hours,
                "StockOptionLevel": stock_level,
                "TotalWorkingYears": total_working_years,
                "TrainingTimesLastYear": training_times,
                "WorkLifeBalance": work_life,
                "YearsAtCompany": years_at_company,
                "YearsInCurrentRole": years_in_role,
                "YearsSinceLastPromotion": years_since_promotion,
                "YearsWithCurrManager": years_with_manager
            }
            
            try:
                response = requests.post(f"{API_URL}/add_employee", json=payload, timeout=10)
                
                if response.status_code == 200:
                    resp_data = response.json()
                    new_id_created = resp_data.get("id")
                    final_data = resp_data.get("data", payload)
                    final_data['id'] = new_id_created # Ensure ID is correct
                    
                    st.success(f"✅ Employee registered successfully! Assigned ID: {new_id_created}")
                    
                    # Add to session state list for verification
                    st.session_state.added_employees_list.append(final_data)
                    
                else:
                    try:
                        error_detail = response.json().get("detail", response.text)
                    except Exception:
                        error_detail = response.text
                    st.error(f"Error: {error_detail}")
                    
            except Exception as e:
                st.error(f"Network Error: {e}")

    # Display added employees in this session
    if st.session_state.added_employees_list:
        st.markdown("### 📋 Recently Added Employees (Session)")
        st.info("These are the employees added during this session. You can review their details below.")
        
        # Iterate in reverse to show newest first
        for i, emp in enumerate(reversed(st.session_state.added_employees_list)):
            with st.expander(f"👤 ID: {emp.get('id')} - {emp.get('JobRole')} ({emp.get('Department')})", expanded=(i==0)):
                # Display key info in columns
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Monthly Income", f"{emp.get('MonthlyIncome')}€")
                c2.metric("Age", emp.get('Age'))
                c3.metric("Years at Company", emp.get('YearsAtCompany'))
                c4.metric("Job Satisfaction", f"{emp.get('JobSatisfaction')}/4")
                
                st.dataframe(pd.DataFrame([emp]), width="stretch", hide_index=True)
