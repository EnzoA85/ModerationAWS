import streamlit as st

st.set_page_config(page_title="Content Moderator Pro", page_icon=":camera:", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title(":camera_with_flash: Content Moderator Pro")
st.header(":mag: Analysez et modérez votre contenu en un clic !")
st.caption(":warning: Veuillez configurer vos credentials AWS dans la barre latérale")

if "show_keys" not in st.session_state:
    st.session_state.show_keys = False


def toggle_visibility():
    st.session_state.show_keys = not st.session_state.show_keys

with st.sidebar:
    st.title(":gear: Configuration")
    st.write(":key: Credentials AWS")
    st.button(":open_file_folder: Charger credentials depuis .env")
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
        }
        </style>
    """

    st.markdown(button_style, unsafe_allow_html=True)

    with st.form("login_form"):
        access_key = st.text_input("Access Key", type="password" if not st.session_state.show_keys else "default")
        secret_key = st.text_input("Secret Key", type="password" if not st.session_state.show_keys else "default")
        bucket_name = st.text_input("Nom du bucket S3")



        # Bouton de validation
        st.form_submit_button("Se Connecter")
