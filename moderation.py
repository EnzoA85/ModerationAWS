import os, cv2, boto3, time, urllib.request, json
from dotenv import load_dotenv

#Fonction de création de session AWS
def get_aws_session():
    # Charge les variables d'environnement depuis .env.
    load_dotenv()

    # Crée une session AWS avec les clés d'accès et la région définies dans les variables d'environnement.
    aws_session = boto3.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),        # Récupère l'ID de clé d'accès depuis les variables d'environnement.
        aws_secret_access_key=os.getenv("SECRET_KEY"),    # Récupère la clé d'accès secrète depuis les variables d'environnement.
        region_name="us-east-1"                           # Spécifie la région AWS à utiliser.
    )
    
    # Retourne l'objet session créé.
    return aws_session


#Fonction instancier client S3 et création bucket
def create_S3User_bucket(bucketname):
    session = boto3.Session(aws_access_key_id=os.getenv("ACCESS_KEY"), aws_secret_access_key=os.getenv("SECRET_KEY"))
    s3 = session.resource("s3")
    bucket = s3.create_bucket(Bucket=bucketname)


#Fonction d'analyse du type du fichier (image ou vidéo)
def check_filetype(filename):   
    # Vérifie si le fichier a une extension
    if '.' not in filename:
        return None
    
    # Extrait l'extension du fichier
    extension = os.path.splitext(filename)[-1].lower().lstrip('.')
    
    # Détermine le type de fichier en fonction de l'extension
    image_extensions = {"jpg", "jpeg", "png", "tiff", "svg", "bmp", "gif"}
    video_extensions = {"mp4", "avi", "mkv", "mov", "wmv", "flv"}
    
    if extension in image_extensions:
        filetype = "image"
    elif extension in video_extensions:
        filetype = "vidéo"
    else:
        filetype = None
    
    return filetype


#Fonction d'extraction d'image d'une vidéo
def extract_frame_video(video_path, frame_id):
    # Ouvre la vidéo à partir du chemin fourni.
    video = cv2.VideoCapture(video_path)

    # Positionne le lecteur vidéo sur l'image spécifiée par frame_id.
    video.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

    # Lit l'image actuelle.
    ret, image = video.read()

    # Si la lecture réussit (ret est True), retourne l'image.
    # Sinon, retourne None.
    return image if ret else None


#Fonction pour modérer une image (reconnaitre les pb)
def moderate_image(image_path, aws_service):
    # Lire l'image en mode binaire
    with open(image_path, "rb") as image_file:
        image_bytes = image_file.read()

    # Appel au service AWS Rekognition
    response = aws_service.detect_moderation_labels(Image={"Bytes": image_bytes})

    # Extraire les étiquettes de modération
    labels = [label["Name"] for label in response.get("ModerationLabels", [])]

    return labels


#Fonction pour identifier les objets d'une image (les 10 plus sur)
def detect_objects(image_path, aws_service):
    # Ouvrir l'image en mode binaire
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Appeler l'API Rekognition pour détecter les objets
    response = aws_service.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10,  # On limite à 10 objets détectés
        MinConfidence=50  # Confiance minimale de 50%
    )

    # Extraire les noms des objets détectés avec la plus haute confiance
    labels = response['Labels']

    # Trier les labels par confiance et prendre les 10 premiers
    top_labels = sorted(labels, key=lambda x: x['Confidence'], reverse=True)[:10]

    # Retourner les noms des objets détectés
    return [label['Name'] for label in top_labels]