import streamlit as st
import os
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(page_title="Content Moderator Pro", page_icon=":camera:", layout="centered")

st.title(":camera_with_flash: Content Moderator Pro")
st.header(":mag: Analysez et modérez votre contenu en un clic !")
st.caption(":warning: Veuillez configurer vos credentials AWS dans la barre latérale")

if "show_keys" not in st.session_state:
    st.session_state.show_keys = False


def toggle_visibility():
    st.session_state.show_keys = not st.session_state.show_keys


# ---- BARRE LATÉRALE ----
with st.sidebar:
    st.title(":gear: Configuration")
    st.write(":key: Credentials AWS")

    # Bouton pour charger les credentials depuis .env
    if st.button(":open_file_folder: Charger credentials depuis .env"):
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("AWS_BUCKET_NAME")

        if access_key and secret_key and bucket_name:
            st.session_state.access_key = access_key
            st.session_state.secret_key = secret_key
            st.session_state.bucket_name = bucket_name
            st.success("✅ Credentials chargés avec succès depuis .env !")
        else:
            st.error("❌ Erreur : Le fichier .env ne contient pas toutes les informations nécessaires.")

    with st.form("login_form"):
        access_key = st.text_input("Access Key", type="password" if not st.session_state.show_keys else "default")
        secret_key = st.text_input("Secret Key", type="password" if not st.session_state.show_keys else "default")
        bucket_name = st.text_input("Nom du bucket S3")

        st.form_submit_button("Se Connecter")

# Types de fichiers acceptés
accepted_formats = ["png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"]
max_file_size = 50 * 1024 * 1024  # 50 MB

uploaded_file = st.file_uploader("Choisissez un fichier (image ou vidéo)", type=accepted_formats)

if uploaded_file:
    # Sélection du fichier
    st.markdown("""
    <h4 style="text-align: left; color:#20a08d; font-size: 15px">
    <strong>Sélection du fichier</strong>
    </h4>
    """, unsafe_allow_html=True)

    # Afficher un spinner pendant l'analyse
    with st.spinner("🔍 Analyse en cours..."):
        time.sleep(2)  # Simule un traitement

        # Vérification de la taille du fichier
        uploaded_file.seek(0, os.SEEK_END)  # Aller à la fin du fichier
        file_size = uploaded_file.tell()  # Obtenir la taille
        uploaded_file.seek(0)  # Revenir au début

        if file_size > max_file_size:
            st.error("❌ Erreur : Le fichier dépasse la limite de 50 Mo.")
        else:
            st.success("✅ Fichier valide ! Prêt pour l'analyse.")
            
            # Affichage de l'image ou de la vidéo
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension in ["png", "jpg", "jpeg", "gif"]:
                st.image(uploaded_file, caption="Image sélectionnée", use_column_width=True)
            elif file_extension in ["mp4", "mov", "avi"]:
                st.video(uploaded_file)