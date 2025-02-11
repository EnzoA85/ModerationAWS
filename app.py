import streamlit as st
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Content Moderator Pro", page_icon=":camera:", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title(":camera_with_flash: Content Moderator Pro")
st.header(":mag: Analysez et modérez votre contenu en un clic !")
st.caption(":warning: Veuillez configurer vos credentials AWS dans la barre latérale")

if "show_keys" not in st.session_state:
    st.session_state.show_keys = False

def toggle_visibility():
    st.session_state.show_keys = not st.session_state.show_keys

# Chargement des credentials depuis le fichier .env
def load_credentials_from_env():
    try:
        load_dotenv()  # Charge le fichier .env
        access_key = os.getenv("ACCESS_KEY")
        secret_key = os.getenv("SECRET_KEY")
        bucket_name = os.getenv("AWS_BUCKET_NAME")

        if access_key and secret_key and bucket_name:
            st.session_state.access_key = access_key
            st.session_state.secret_key = secret_key
            st.session_state.bucket_name = bucket_name
            st.success("Credentials chargés avec succès depuis le fichier .env!")
        else:
            st.error("Erreur : Le fichier .env ne contient pas toutes les informations nécessaires.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des credentials : {e}")

with st.sidebar:
    st.title(":gear: Configuration")
    st.write(":key: Credentials AWS")
    
    # Bouton pour charger les credentials depuis .env
    if st.button(":open_file_folder: Charger credentials depuis .env"):
        load_credentials_from_env()

    # Utilisation de HTML/CSS pour styliser un bouton en vert
    button_style = """
        <style>
        div.stButton > button {
            background-color: green !important;
            color: white !important;
            padding: 10px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: darkgreen !important;
            color: white !important;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # Formulaire pour la méthode manuelle
    with st.form("login_form"):
        access_key = st.text_input("Access Key", value=st.session_state.get("access_key", ""), type="password" if not st.session_state.show_keys else "default")
        secret_key = st.text_input("Secret Key", value=st.session_state.get("secret_key", ""), type="password" if not st.session_state.show_keys else "default")
        bucket_name = st.text_input("Nom du bucket S3", value=st.session_state.get("bucket_name", ""))

        # Bouton de validation
        st.form_submit_button("Se Connecter")