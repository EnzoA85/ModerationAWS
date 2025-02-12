import streamlit as st, os, time
from dotenv import load_dotenv
from moderation import process_media, get_aws_session

st.set_page_config(page_title="Content Moderator Pro", page_icon=":camera:", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title(":camera_with_flash: Content Moderator Pro")
st.header(":mag: Analysez et modérez votre contenu en un clic !")
st.caption(":warning: Veuillez configurer vos credentials AWS dans la barre latérale")

if "show_keys" not in st.session_state:
    st.session_state.show_keys = False

if "connected" not in st.session_state:
    st.session_state.connected = False  # Variable de connexion

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
            st.session_state.connected = True  # Connexion réussie
            st.success("Credentials chargés avec succès depuis le fichier .env!")
        else:
            st.error("Erreur : Le fichier .env ne contient pas toutes les informations nécessaires.")
    except Exception as e:
        st.error(f"Erreur lors du chargement des credentials : {e}")
aws_session = get_aws_session()
rekognition = aws_session.client("rekognition")
transcribe = aws_session.client("transcribe")
comprehend = aws_session.client("comprehend")

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
        submit_button = st.form_submit_button("Se Connecter")

        # Vérification de la connexion
        if submit_button:
            if access_key and secret_key and bucket_name:
                st.session_state.access_key = access_key
                st.session_state.secret_key = secret_key
                st.session_state.bucket_name = bucket_name
                st.session_state.connected = True  # Connexion réussie
                st.success("Connexion réussie !")
            else:
                st.error("Erreur : Veuillez remplir tous les champs pour vous connecter.")


# ---- Affichage de la zone d'upload si connecté ----
if st.session_state.connected:
    # Zone d'upload

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

            # Vérification de la taille du fichier
            uploaded_file.seek(0, os.SEEK_END)  # Aller à la fin du fichier
            file_size = uploaded_file.tell()  # Obtenir la taille
            uploaded_file.seek(0)  # Revenir au début

            if file_size > max_file_size:
                st.error("❌ Erreur : Le fichier dépasse la limite de 50 Mo.")
            else:
                st.success("✅ Fichier valide ! Prêt pour l'analyse.")
                
                # Appel de la fonction process_media pour analyser le fichier
                analysis_result = process_media(uploaded_file, rekognition, transcribe, comprehend)
                
                # Affichage de l'image ou de la vidéo
                file_extension = uploaded_file.name.split(".")[-1].lower()

                if file_extension in ["png", "jpg", "jpeg", "gif"]:
                    st.image(uploaded_file, caption="Image sélectionnée", use_container_width=True)
                elif file_extension in ["mp4", "mov", "avi"]:
                    st.video(uploaded_file)
                
                # Extraction des objets (hashtags)
                analysis_result, file_type = process_media(uploaded_file, rekognition, transcribe, comprehend)
                hashtags = analysis_result.get('objects', [])
                
                if hashtags:
                    # Création d'une bulle bleue pour chaque hashtag
                    hashtags_html = ""
                    for hashtag in hashtags:
                        hashtags_html += f"""
                        <div style="display: inline-block; background-color: rgba(0, 123, 255, 0.5); color: white; padding: 5px 10px; margin: 5px; border-radius: 12px; font-size: 14px;">
                            #{hashtag}
                        </div>
                        """
                    # Afficher les hashtags en une seule ligne (à la suite)
                    st.markdown(hashtags_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ Vous devez vous connecter avec vos credentials AWS pour accéder à la zone d'upload.")
