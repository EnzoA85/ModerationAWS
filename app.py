import streamlit as st, os
from dotenv import load_dotenv
from moderation import process_media, get_aws_session

st.set_page_config(page_title="Content Moderator Pro", page_icon=":camera:", layout="centered")

st.title(":camera_with_flash: Content Moderator Pro")
st.header(":mag: Analysez et modérez votre contenu en un clic !")
st.caption(":warning: Veuillez configurer vos credentials AWS dans la barre latérale")

if "connected" not in st.session_state:
    st.session_state.connected = False

def load_credentials():
    load_dotenv()
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    bucket_name = os.getenv("AWS_BUCKET_NAME")

    if access_key and secret_key and bucket_name:
        st.session_state.access_key = access_key
        st.session_state.secret_key = secret_key
        st.session_state.bucket_name = bucket_name
        st.session_state.connected = True
        st.success("Credentials chargés avec succès.")
    else:
        st.error("Le fichier .env est incomplet.")

aws_session = get_aws_session()
rekognition = aws_session.client("rekognition")
transcribe = aws_session.client("transcribe")
comprehend = aws_session.client("comprehend")

with st.sidebar:
    st.title(":gear: Configuration")
    st.write(":key: Credentials AWS")
    
    if st.button(":open_file_folder: Charger credentials depuis .env"):
        load_credentials()

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

    with st.form("login_form"):
        access_key = st.text_input("Access Key", type="password" if not st.session_state.get("show_keys") else "default")
        secret_key = st.text_input("Secret Key", type="password" if not st.session_state.get("show_keys") else "default")
        bucket_name = st.text_input("Nom du bucket S3", value=st.session_state.get("bucket_name", ""))

        if st.form_submit_button("Se Connecter"):
            if access_key and secret_key and bucket_name:
                st.session_state.access_key = access_key
                st.session_state.secret_key = secret_key
                st.session_state.bucket_name = bucket_name
                st.session_state.connected = True
                st.success("Connexion réussie !")
            else:
                st.error("Tous les champs doivent être remplis.")

if st.session_state.connected:
    accepted_formats = ["png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"]
    max_file_size = 50 * 1024 * 1024

    uploaded_file = st.file_uploader("Choisissez un fichier (image ou vidéo)", type=accepted_formats)

    if uploaded_file:
        uploaded_file.seek(0, os.SEEK_END)
        file_size = uploaded_file.tell()
        uploaded_file.seek(0)

        if file_size > max_file_size:
            st.error("Le fichier dépasse la limite de 50 Mo.")
        else:
            st.success("Fichier valide !")

            analysis_result, file_type = process_media(uploaded_file, rekognition, transcribe, comprehend)
            hashtags = analysis_result.get('objects', [])
            moderation = analysis_result.get('moderation', [])

            if moderation:
                st.markdown("""
                <div style="background-color: rgba(255, 0, 0, 0.5); padding: 20px; border-radius: 10px; color: white;">
                    <h2>⚠️ Contenu bloqué</h2>
                    <p>Le contenu a été bloqué en raison de la détection de thèmes sensibles.</p>
                </div>
                """, unsafe_allow_html=True)
                for theme in moderation:
                    st.write(f"- {theme}")
                st.stop()

            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension in ["png", "jpg", "jpeg", "gif"]:
                st.image(uploaded_file, caption="Image sélectionnée", use_container_width=True)
            elif file_extension in ["mp4", "mov", "avi"]:
                st.video(uploaded_file)

            if hashtags:
                hashtags_html = "".join(f"""
                    <div style="display: inline-block; background-color: rgba(0, 123, 255, 0.5); color: white; padding: 5px 10px; margin: 5px; border-radius: 12px; font-size: 14px;">
                        #{hashtag}
                    </div>
                """ for hashtag in hashtags)
                st.markdown(hashtags_html, unsafe_allow_html=True)
else:
    st.warning("⚠️ Vous devez vous connecter pour accéder à la zone d'upload.")
