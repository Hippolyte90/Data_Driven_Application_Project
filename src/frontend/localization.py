"""
Localization module for the application.
Handles translation logic using a manual dictionary and an offline NLP model.
"""
import streamlit as st
from transformers import pipeline

LANGUAGE_OPTIONS = ["EN", "FR"]

# Dictionary for manual translations (English -> French)
MANUAL_TRANSLATIONS = {
    "HR Login": "Connexion RH",
    "Sign up": "Inscription",
    "Email": "Email",
    "Password": "Mot de passe",
    "Account created! Please log in.": "Compte créé ! Veuillez vous connecter.",
    "Error during registration.": "Erreur lors de l'inscription.",
    "Already registered? Log in": "Déjà inscrit ? Se connecter",
    "Log in": "Connexion",
    "Login error (invalid server response).": "Erreur de connexion (réponse invalide du serveur).",
    "Incorrect credentials.": "Identifiants incorrects.",
    "Not registered yet? Sign up": "Pas encore inscrit ? S'inscrire",
    "Dashboard": "Tableau de bord",
    "Add Employee": "Ajouter Employé",
    "Help": "Aide",
    "Language": "Langue",
    "Request Demo": "Demander une démo",
    "Thank you, we will contact you for a demo.": "Merci, nous vous contacterons pour une démo.",
    "Log out": "Se déconnecter",
    "Error loading dashboard:": "Erreur en chargeant le dashboard:",
    "Error loading the add form:": "Erreur en chargeant le formulaire d'ajout:",
    "Error loading help page:": "Erreur en chargeant la page d'aide:",
    "Search": "Rechercher",
    "Employee ID": "ID Employé",
    "Department": "Département",
    "Sales": "Ventes",
    "Research & Development": "R&D",
    "Human Resources": "Ressources Humaines",
    "All": "Tous",
    "Return to Home": "Retour à l'accueil",
    "Search Result": "Résultat de la recherche",
    "Performance Hub": "Centre de Performance",
    "Register New Employee": "Enregistrer un nouvel employé",
    "Help & Contacts": "Aide & Contacts",
}

@st.cache_resource
def load_translator(source_lang, target_lang):
    """
    Loads the translation model (Helsinki-NLP) and caches it.
    The model is downloaded locally upon first use.
    """
    model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
    try:
        # pipeline handles downloading and disk caching automatically
        return pipeline("translation", model=model_name)
    except Exception as e:
        st.error(f"Error loading translation model ({source_lang}->{target_lang}): {e}")
        return None

def translate_label(label: str) -> str:
    """
    Translates a given label based on the selected language in session state.
    Prioritizes manual translations, then falls back to the NLP model.
    """
    if not label:
        return label
    
    lang = st.session_state.get("lang_select", "EN").upper()
    
    # If language is EN, return label (assumed to be in EN in the code)
    if lang == "EN":
        return label
        
    # If language is FR
    if lang == "FR":
        # 1. Manual dictionary (priority)
        if label in MANUAL_TRANSLATIONS:
            return MANUAL_TRANSLATIONS[label]
            
        # 2. Session cache for automatic translations already done
        if "auto_translations" not in st.session_state:
            st.session_state.auto_translations = {}
        
        if label in st.session_state.auto_translations:
            return st.session_state.auto_translations[label]
            
        # 3. Automatic translation (EN -> FR)
        translator = load_translator("en", "fr")
        if translator:
            try:
                res = translator(label)
                translated_text = res[0]['translation_text']
                st.session_state.auto_translations[label] = translated_text
                return translated_text
            except Exception:
                pass
                
    return label

t = translate_label