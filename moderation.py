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
    session = boto3.Session(
        aws_access_key_id=os.getenv("ACCESS_KEY"),
        aws_secret_access_key=os.getenv("SECRET_KEY"),
        region_name="eu-west-1"  # Remplacez par votre région AWS
    )
    s3 = session.resource("s3")

    bucket = s3.create_bucket(
        Bucket=bucketname,
        CreateBucketConfiguration={
            'LocationConstraint': "eu-west-1"  # Remplacez par votre région AWS
        }
    )

    return bucket


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


#Fonction pour détecter les célébrités sur une image
def detect_celebrities(image_path, aws_service):
    # Ouvrir l'image en mode binaire
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Appeler l'API Rekognition pour détecter les célébrités
    response = aws_service.recognize_celebrities(
        Image={'Bytes': image_bytes}
    )

    # Extraire les noms des célébrités détectées
    celebrities = response.get('CelebrityFaces', [])

    # Limiter à 10 célébrités maximum
    top_celebrities = [celebrity['Name'] for celebrity in celebrities[:10]]

    # Retourner les résultats
    return top_celebrities


#Fonction pour détecter les émotions
def detect_emotions(image_path, aws_service):
    # Ouvrir l'image en mode binaire
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Appeler l'API Rekognition pour détecter les visages avec tous les attributs
    response = aws_service.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']  # Demande de tous les attributs, y compris les émotions
    )

    # Initialiser la liste pour stocker les résultats
    faces_info = []

    # Parcourir les visages détectés
    for face_detail in response['FaceDetails']:
        face_data = {}

        # Récupérer le genre et son niveau de confiance
        gender = face_detail['Gender']
        face_data['Gender'] = {
            'Value': gender['Value'],
            'Confidence': round(gender['Confidence'], 2)
        }

        # Récupérer l'âge estimé (plage)
        age_range = face_detail['AgeRange']
        face_data['AgeRange'] = {
            'Low': age_range['Low'],
            'High': age_range['High']
        }

        # Récupérer les 3 émotions principales et leurs niveaux de confiance
        emotions = sorted(face_detail['Emotions'], key=lambda x: x['Confidence'], reverse=True)
        top_3_emotions = emotions[:3]  # Sélectionner les 3 émotions principales
        face_data['Emotions'] = [{
            'Type': emotion['Type'],
            'Confidence': round(emotion['Confidence'], 2)
        } for emotion in top_3_emotions]

        # Ajouter le visage détecté avec ses informations dans la liste
        faces_info.append(face_data)

        # Affichage des informations sur chaque visage détecté
        print("[INFO] Visage détecté:")
        print(f"  - Genre: {gender['Value']} (confiance: {round(gender['Confidence'], 2)}%)")
        print(f"  - Âge estimé: {age_range['Low']}-{age_range['High']} ans")
        print("  - Émotions principales:")
        for emotion in top_3_emotions:
            print(f"    * {emotion['Type']}: {round(emotion['Confidence'], 2)}%")
        print("---")

    # Retourner la liste des informations des visages détectés
    return faces_info

def summarize_emotions(faces_info):
    # Initialisation des variables
    total_faces = len(faces_info)
    emotion_stats = {}  # Dictionnaire pour compter les émotions et leur confiance moyenne
    age_stats = {'min': float('inf'), 'max': float('-inf'), 'sum': 0}  # Statistiques d'âge
    gender_stats = {'Male': 0, 'Female': 0}  # Compteur de genres

    dominant_emotion = {'Type': None, 'Confidence': 0}  # Émotion dominante
    total_emotions_confidence = 0  # Somme des confiances des émotions pour calculer l'émotion dominante
    emotion_count = 0  # Compteur pour les émotions

    # Analyser chaque visage dans les informations fournies
    for face in faces_info:
        # Calcul de l'âge moyen pour chaque visage
        age_range = face['AgeRange']
        age_mean = (age_range['Low'] + age_range['High']) / 2
        age_stats['sum'] += age_mean
        age_stats['min'] = min(age_stats['min'], age_mean)
        age_stats['max'] = max(age_stats['max'], age_mean)

        # Mise à jour des statistiques de genre
        gender = face['Gender']['Value']
        gender_stats[gender] += 1

        # Analyser les émotions de chaque visage
        for emotion in face['Emotions']:
            # Si la confiance est > 50%, on la prend en compte
            if emotion['Confidence'] > 50:
                emotion_type = emotion['Type']
                confidence = emotion['Confidence']

                # Mise à jour des statistiques d'émotions
                if emotion_type not in emotion_stats:
                    emotion_stats[emotion_type] = {'count': 0, 'confidence_sum': 0}
                emotion_stats[emotion_type]['count'] += 1
                emotion_stats[emotion_type]['confidence_sum'] += confidence

                # Mise à jour de l'émotion dominante
                if confidence > dominant_emotion['Confidence']:
                    dominant_emotion = {'Type': emotion_type, 'Confidence': confidence}

                # Calcul de la confiance moyenne des émotions
                total_emotions_confidence += confidence
                emotion_count += 1

    # Calcul de l'émotion dominante
    dominant_emotion_avg_confidence = dominant_emotion['Confidence']

    # Calcul des statistiques d'âge
    if total_faces > 0:
        age_stats['average'] = age_stats['sum'] / total_faces
    else:
        age_stats['average'] = 0

    # Calcul de la confiance moyenne des émotions
    if emotion_count > 0:
        avg_emotion_confidence = total_emotions_confidence / emotion_count
    else:
        avg_emotion_confidence = 0

    # Retourner le résumé des émotions
    return {
        'total_faces': total_faces,
        'dominant_emotion': dominant_emotion['Type'],
        'dominant_emotion_confidence': dominant_emotion_avg_confidence,
        'emotion_stats': {
            'count': emotion_stats,
            'average_confidence': avg_emotion_confidence
        },
        'age_stats': age_stats,
        'gender_stats': gender_stats
    }


import os
import time
import json
import boto3
import subprocess

def extract_audio_from_video(video_path, audio_path):
    """
    Extrait l'audio d'une vidéo en utilisant ffmpeg.
    
    Paramètres :
    - video_path (str) : Chemin de la vidéo en entrée.
    - audio_path (str) : Chemin de sortie pour l'audio extrait.
    """
    command = f"ffmpeg -i {video_path} -vn -acodec mp3 {audio_path} -y"
    subprocess.run(command, shell=True, check=True)

def get_text_from_speech(video_filename, aws_service, job_name, bucket_name):
    """
    Transcrit l'audio extrait d'une vidéo en texte avec AWS Transcribe.

    Étapes :
    1. Extraction de l'audio depuis la vidéo.
    2. Téléversement de l'audio sur S3.
    3. Démarrage et suivi du job de transcription AWS Transcribe.
    4. Récupération du texte transcrit.

    Paramètres :
    - video_filename (str) : Chemin du fichier vidéo.
    - aws_service (boto3.client) : Client AWS Transcribe.
    - job_name (str) : Nom du job de transcription.
    - bucket_name (str) : Nom du bucket S3.

    Retourne :
    - str : Texte transcrit.
    """

    # 1️⃣ Extraire l'audio
    audio_filename = video_filename.replace(".mp4", ".mp3")
    extract_audio_from_video(video_filename, audio_filename)

    # 2️⃣ Téléverser sur S3
    s3_client = boto3.client("s3")
    s3_key = f"audio/{os.path.basename(audio_filename)}"
    s3_client.upload_file(audio_filename, bucket_name, s3_key)
    file_uri = f"s3://{bucket_name}/{s3_key}"

    # 3️⃣ Lancer AWS Transcribe
    aws_service.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": file_uri},
        MediaFormat="mp3",
        LanguageCode="fr-FR"
    )

    # 4️⃣ Vérifier le statut du job
    while True:
        response = aws_service.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]

        if status in ["COMPLETED", "FAILED"]:
            break
        time.sleep(5)

    if status == "COMPLETED":
        transcript_uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
        
        # Télécharger et lire le fichier JSON du transcript
        transcript_json = boto3.client("s3").get_object(Bucket=bucket_name, Key=s3_key)
        transcript_data = json.loads(transcript_json['Body'].read().decode("utf-8"))
        return transcript_data["results"]["transcripts"][0]["transcript"]

    else:
        raise Exception("Échec de la transcription")

# 💡 Utilisation :
# aws_session = get_aws_session()
# transcribe_client = aws_session.client("transcribe")
# text = get_text_from_speech("video.mp4", transcribe_client, "transcription_job", "my-s3-bucket")
# print(text)
