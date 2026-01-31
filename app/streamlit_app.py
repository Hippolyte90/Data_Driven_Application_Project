"""
Main entry point for the Streamlit frontend application.
Handles authentication, navigation, and page rendering.
"""
import base64
from pathlib import Path
import sys
import os

import streamlit as st
import requests
from transformers import pipeline

# Ensure project root is on sys.path so `import src` works inside containers
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import *

API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="HR Management System",
                   page_icon="https://www.joomeo.com/favicon.ico",
                   layout="wide")

# Function to upload the CSS
def local_css(file_path: Path):
    if not file_path.exists():
        st.warning(f"CSS not found : {file_path}")
        return
    with file_path.open(encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


style_path = (Path(__file__).resolve().parent / "assets/style.css").resolve()
#local_css(style_path)


# helper to rerun in a Streamlit-version-safe way
def _try_rerun():
    if hasattr(st, "experimental_rerun"):
        try:
            st.experimental_rerun()
        except Exception:
            pass
    elif hasattr(st, "rerun"):
        try:
            st.rerun()
        except Exception:
            pass
    else:
        # no rerun support: rely on session_state changes; user may refresh
        pass


# --- AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # center authentication UI in the middle column
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.title("HR Login")

        # Ensure a flag that indicates registration completed
        if "registered" not in st.session_state:
            st.session_state.registered = False

        # Step 1: Registration
        if not st.session_state.registered:
            st.subheader("Sign up")
            email_reg = st.text_input("Email", key="reg_email")
            pw_reg = st.text_input("Password", type="password", key="reg_pw")
            if st.button("Sign up"):
                if not email_reg or not pw_reg:
                    st.error("Incorrect credentials.")
                else:
                    res = requests.post(f"{API_URL}/register", json={"email": email_reg, "password": pw_reg})
                    if res.status_code == 200:
                        st.success("Account created! Please log in.")
                        # remember email for the login step
                        st.session_state.registered = True
                        st.session_state.prefill_email = email_reg
                        _try_rerun()
                    else:
                        # try to show backend error message
                        try:
                            err = res.json().get("detail")
                        except Exception:
                            err = "Error during registration."
                        st.error(err)
            # Allow users who already have an account to go directly to login
            if st.button("Already registered? Log in"):
                st.session_state.registered = True
                _try_rerun()

        # Step 2: Login (display after registration)
        else:
            st.subheader("Log in")
            prefill = st.session_state.get("prefill_email", "")
            email_log = st.text_input("Email", key="log_email", value=prefill)
            pw_log = st.text_input("Password", type="password", key="log_pw")
            if st.button("Log in"):
                if not email_log or not pw_log:
                    st.error("Incorrect credentials.")
                else:
                    res = requests.post(f"{API_URL}/login", json={"email": email_log, "password": pw_log})
                    try:
                        payload = res.json()
                    except Exception:
                        st.error("Login error (invalid server response).")
                        st.stop()
                    if payload.get("status") == "success":
                        st.session_state.logged_in = True
                        _try_rerun()
                    else:
                        fallback_err = "Incorrect credentials."
                        st.error(payload.get("message", fallback_err))
            # If user hasn't registered yet, allow returning to the inscription form
            if st.button("Not registered yet? Sign up"):
                st.session_state.registered = False
                _try_rerun()

    st.stop()


# Header: logo left, centered menu, globe + demo button right
PAGE_KEYS = ["Dashboard", "Add Employee", "Help"]
if "page" not in st.session_state:
    st.session_state.page = PAGE_KEYS[0]
    
    
    
# Page key for departement-specific views
DEPT_PAGE_KEYS = ["All","Sales", "Research & Development", "Human Resources"]
if "dept_page" not in st.session_state:
    st.session_state.dept_page = DEPT_PAGE_KEYS[0]

dept = st.session_state.get("dept_page", "All")

# minimal CSS to style header area
st.markdown(
    """
    <style>
    .top-bar { display:flex; align-items:center; justify-content:space-between; padding:10px 20px; background:#fff7f6; border-bottom:4px solid #6f1436; }
    .top-left { display:flex; align-items:center; gap:12px; }
    .top-center { display:flex; gap:24px; justify-content:center; flex:1; }
    .nav-item { font-weight:600; color:#222; }
    .request-btn { background:#ff2d55; color:#fff; padding:8px 14px; border-radius:8px; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

page = st.session_state.page

#left_col, right_col = st.columns([1, 6], gap="large")

with st.sidebar:
    st.markdown('<div class="top-left">', unsafe_allow_html=True)
    st.markdown("<div style='margin-top:-24px;'></div>", unsafe_allow_html=True)
    try:
        logo_path = Path("frontend/assets/logo_aut.png")
        logo_bytes = logo_path.read_bytes()
        logo_b64 = base64.b64encode(logo_bytes).decode("ascii")
        st.markdown( "# ↗️ Perform Employee Track ", unsafe_allow_html=True)
        st.markdown("---")
    except Exception:
        st.image("https://www.joomeo.com/favicon.ico", width=80)
        st.markdown("# ↗️ Perform Employee Track ", unsafe_allow_html=True)
        st.markdown("---")
        
    
    st.selectbox("Department", DEPT_PAGE_KEYS, key="dept_page")
    st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Employee Search")

    def run_search():
        st.session_state.search_emp_id = st.session_state.sidebar_search_input
        st.session_state.page = "Dashboard"
        st.session_state.dept_page = "All"

    st.number_input("Employee ID", min_value=1, step=1, key="sidebar_search_input")
    st.button("🔎 Search", key="sidebar_search_btn", on_click=run_search)
    st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



    if st.button("Log out"):
        st.session_state.update({"logged_in": False})
        _try_rerun()

st.markdown("<div style='margin-top:-24px;'></div>", unsafe_allow_html=True)
# Try to use streamlit-option-menu for a nicer horizontal menu; fallback to buttons
try:
    from streamlit_option_menu import option_menu
    menu_labels = PAGE_KEYS
    default_index = PAGE_KEYS.index(st.session_state.page) if st.session_state.page in PAGE_KEYS else 0
    selected_label = option_menu(
        None,
        menu_labels,
        icons=["house", "person-plus", "info-circle"],
        menu_icon="cast",
        default_index=default_index,
        orientation="horizontal",
        styles={
            "container": {"padding": "0px 0px", "background": "transparent"},
            "nav-link": {"font-size": "20px", "text-align": "center", "margin": "0px 8px"},
            "nav-link-selected": {"background-color": "#461ced", "color": "white"},
        },
    )
    selected_key = st.session_state.page
    if selected_label in menu_labels:
        selected_key = PAGE_KEYS[menu_labels.index(selected_label)]
    if selected_key != st.session_state.page:
        st.session_state.page = selected_key
        _try_rerun()
except Exception:
    # fallback to simple buttons
    nav1, nav2, nav3 = st.columns([1, 1, 1])
    with nav1:
        if st.button("Dashboard"):
            st.session_state.page = "Dashboard"
            _try_rerun()
    with nav2:
        if st.button("Add Employee"):
            st.session_state.page = "Add Employee"
            _try_rerun()
    with nav3:
        if st.button("Help"):
            st.session_state.page = "Help"
            _try_rerun()
            
            
if page == "Dashboard":
    try:
        if dept == "All":
            from src.frontend.dashboard_view import render_dashboard
            render_dashboard()
        
        elif dept == "Sales":
            from src.frontend.dashboard_view import render_sales_data
            render_sales_data()
        elif dept == "Research & Development":
            from src.frontend.dashboard_view import render_rd_data
            render_rd_data()
        elif dept == "Human Resources":
            from src.frontend.dashboard_view import render_hr_data
            render_hr_data()
        
    except Exception as e:
        st.error(f"Error loading dashboard: {e}") 

elif page == "Add Employee":
    try:
        from src.frontend.add_employee_view import render_add_employee
        render_add_employee()
    except Exception as e:
        st.error(f"Error loading the add form: {e}")

elif page == "Help":
    try:
        from src.frontend.help_view import render_help
        render_help()
    except Exception as e:
        st.error(f"Error loading help page: {e}")

st.markdown("<div style='height: 120px'></div>", unsafe_allow_html=True)
st.markdown(" ") 
st.markdown(" ")
st.markdown(" ") 
st.markdown(" ")          
st.markdown(" ")  
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>✨ HR Management System - Developed by Solftware 2026 ✨"
    "</div>",
    unsafe_allow_html=True,
)
