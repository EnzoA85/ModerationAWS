import os, cv2, boto3, time, tempfile

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
    return labels

def process_media(media_file, rekognition, transcribe, comprehend):
    # Utiliser le nom du fichier pour vérifier son type
    file_type = check_filetype(media_file.name)  # Correction ici
    
    if file_type is None:
        return {"error": "Type de fichier non supporté."}, None
    
    results = {"file_type": file_type}

    # Sauvegarder temporairement le fichier
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{media_file.name.split('.')[-1]}") as temp_file:
        temp_file.write(media_file.getbuffer())  # Écrit le contenu de l'UploadedFile dans un fichier temporaire
        temp_file_path = temp_file.name  # Récupère le chemin du fichier temporaire

    # Si le fichier est une image, effectuer les analyses
    if file_type == "image":
        # Passer le chemin du fichier temporaire à la fonction
        results["moderation"] = moderate_image(temp_file_path, rekognition)
        
        # Si des labels de contenu inapproprié sont détectés
        inappropriate_labels = [
            "Explicit Nudity", "Violence", "Abuse", "Hate", "Drugs"
        ]
        detected_labels = results["moderation"]
        
        # Vérifie si des labels inappropriés sont présents
        blocked_content = [label for label in detected_labels if label in inappropriate_labels]

        if blocked_content:
            # Ajouter une alerte rouge
            results["blocked"] = {
                "message": "⚠️ Contenu inapproprié détecté. Le contenu a été bloqué.",
                "reasons": blocked_content  # Liste des raisons
            }
        else:
            # Continuer avec l'analyse d'autres aspects
            results["objects"] = detect_objects(temp_file_path, rekognition)
            results["celebrities"] = detect_celebrities(temp_file_path, rekognition)
            results["emotions"] = detect_emotions(temp_file_path, rekognition)
    
    # Logique pour traiter une vidéo (ajout de l'analyse future si nécessaire)
    elif file_type == "vidéo":
        results["message"] = "Traitement vidéo non encore implémenté."
    
    return results, file_type