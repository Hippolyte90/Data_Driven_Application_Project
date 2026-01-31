"""
View module for the Help & Contacts page.
Displays team information and support details.
"""
import streamlit as st
from pathlib import Path

def render_help():
    """Renders the help page with team cards and contact info."""
    st.title("ℹ️ Help & Contacts")
    st.markdown("### 🤝 Project Team")
    st.write("We are a team of three developers dedicated to this project. Feel free to contact us via LinkedIn for any questions or suggestions.")

    st.markdown("---")

    # --- TEMPLATE CONTACTS ---
    # Get the folder where this script is located (src/frontend) to locate images
    assets_dir = Path(__file__).parent

    # Replace the information below with yours
    team_members = [
        {
            "name": "Hippolyte SODJINOU",
            "role": "Data Scientist/ Developer",
            "linkedin": "https://www.linkedin.com/in/hippolyte-sodjinou/",
            "avatar": str(assets_dir / "hippo.jpg")
        },
        {
            "name": "Nercy chancelle Nisabwe",
            "role": "Data Scientist / Data Analyst",
            "linkedin": "https://www.linkedin.com/in/nercy-chancelle-nisabwe-84572728a/",
            "avatar": str(assets_dir / "nercy.jpg")
        },
        {
            "name": "Danélius D. ADJENIA",
            "role": " Data Scientist/ Developer frontend",
            "linkedin": "https://www.linkedin.com/in/dan%C3%A9lius-d-adjenia/",
            "avatar": str(assets_dir / "danelius.jpg")
        }
    ]

    # Display in 3 columns
    col1, col2, col3 = st.columns(3)
    
    for idx, col in enumerate([col1, col2, col3]):
        member = team_members[idx]
        with col:
            # Use a container to group elements
            with st.container():
                st.image(member["avatar"], width=100)
                st.subheader(member["name"])
                st.caption(member["role"])
                
                # LinkedIn button styled in HTML
                st.markdown(f"""
                    <a href="{member['linkedin']}" target="_blank" style="text-decoration: none;">
                        <div style="
                            background-color: #0077b5;
                            color: white;
                            padding: 8px 12px;
                            border-radius: 5px;
                            text-align: center;
                            font-weight: bold;
                            margin-top: 10px;
                            width: 100%;">
                            LinkedIn 🔗
                        </div>
                    </a>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("### 📞 Technical Support")
    st.info("If you encounter a critical bug, please contact the administrator or open an issue on the project repository.")