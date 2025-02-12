from moderation import process_media, get_aws_session, check_filetype, extract_frame_video, moderate_image, detect_objects, detect_celebrities, detect_emotions, summarize_emotions
from matplotlib import pyplot as plt
import cv2, boto3, json



#Test de la fonction check_filetype
# file_type = check_filetype("assets/tuto_maquillage.mp4")
# file_type = check_filetype("assets/selfie_with_johnny-depp.png")
# print(file_type)



#Test de la fonction extract_frame_video
# TEST_VIDEO_FILE = "assets/tuto_jeux-video.mp4"

# image = extract_frame_video(TEST_VIDEO_FILE, 99)
# if image is not None:
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
#     # Afficher l'image
#     plt.imshow(image_rgb)
#     plt.axis("off")  # Masquer les axes pour une meilleure visualisation
#     plt.show()
# else:
#     print("Impossible d'extraire l'image de la vidéo.")



#Test de la fonction moderate_image
# Obtenir la session AWS à partir de la fonction fournie
# aws_session = get_aws_session()

# # Instanciation du service Rekognition
# rekognition_client = aws_session.client("rekognition")

# # Liste des images à tester
# test_images = [
#     "assets/haine.png",
#     "assets/vulgaire.png",
#     "assets/violence1.png",
#     "assets/no-violence1.png"
# ]

# # Test de la fonction pour chaque image
# for image_path in test_images:
#     print(f"Analyse de {image_path}...")
#     detected_labels = moderate_image(image_path, rekognition_client)
#     print(f"Étiquettes détectées : {detected_labels}\n")



# #Test de la fonction detect_objet
# TEST_IMAGE_FILE = "assets/no-violence4.png"

# # Instancier le service AWS Rekognition
# aws_session = get_aws_session()
# rekognition_client = aws_session.client('rekognition', region_name='us-east-1')

# # Appel à la fonction detect_objects pour récupérer la liste des objets
# detected_objects = detect_objects(TEST_IMAGE_FILE, rekognition_client)

# # Affichage des objets détectés
# print("Objets détectés dans l'image :", detected_objects)



# #Test de la fonction detect_celebrities
# TEST_IMAGE_FILE_1 = "./assets/selfie_with_mariah-carey.png"
# TEST_IMAGE_FILE_2 = "./assets/selfie_with_johnny-depp.png"
# TEST_IMAGE_FILE_3 = "./assets/selfie_with_kanye-west.png"
# # Supposons que vous ayez déjà une session AWS valide
# aws_session = get_aws_session()
# rekognition_client = aws_session.client('rekognition', region_name='us-east-1')

# # Liste des images de test
# test_images = [TEST_IMAGE_FILE_1, TEST_IMAGE_FILE_2, TEST_IMAGE_FILE_3]

# # Pour chaque image, appeler la fonction detect_celebrities et afficher les résultats
# for image_path in test_images:
#     print(f"\nDétection des célébrités dans l'image : {image_path}")
#     celebrities = detect_celebrities(image_path, rekognition_client)
#     print(f"Célébrités détectées : {celebrities}")



# #Test de la fonction detect_emotions et summarize_emotions
# # Définir les chemins des images de test
# TEST_IMAGE_FILE_1 = "./assets/group_selfie_1.jpg"    # Premier selfie de groupe
# TEST_IMAGE_FILE_2 = "./assets/group_selfie_2.jpg"    # Deuxième selfie de groupe
# TEST_IMAGE_FILE_3 = "./assets/group_selfie_3.jpg"    # Troisième selfie de groupe
# TEST_IMAGE_FILE_4 = "./assets/group_selfie_4.jpg"    # Quatrième selfie de groupe

# # Supposons que vous ayez déjà une session AWS valide
# aws_session = get_aws_session()  # Vous pouvez adapter cette fonction selon votre propre configuration
# rekognition_client = aws_session.client('rekognition', region_name='us-east-1')

# # Liste des images de test
# test_images = [TEST_IMAGE_FILE_1, TEST_IMAGE_FILE_2, TEST_IMAGE_FILE_3, TEST_IMAGE_FILE_4]

# # Pour chaque image, appeler la fonction detect_emotions et afficher les résultats
# for image_path in test_images:
#     print(f"\nAnalyse des émotions pour l'image : {image_path}")
    
#     # Analyser les émotions des visages détectés dans l'image
#     faces_info = detect_emotions(image_path, rekognition_client)
    
#     # Afficher les détails des visages détectés
#     for idx, face in enumerate(faces_info, 1):
#         print(f"\n[INFO] Visage {idx} détecté:")
#         print(f"  - Genre: {face['Gender']['Value']} (Confiance: {face['Gender']['Confidence']}%)")
#         print(f"  - Âge estimé: {face['AgeRange']['Low']} - {face['AgeRange']['High']} ans")
#         print(f"  - Émotions détectées :")
#         for emotion in face['Emotions']:
#             print(f"    * {emotion['Type']}: {emotion['Confidence']}%")
    
#     # Générer le résumé des statistiques des émotions
#     summary = summarize_emotions(faces_info)
    
#     # Afficher le résumé des statistiques
#     print("\n[INFO] Résumé des émotions :")
#     print(f"  - Nombre total de visages détectés : {summary['total_faces']}")
#     print(f"  - Émotion dominante : {summary['dominant_emotion']} (Confiance: {summary['dominant_emotion_confidence']}%)")
#     print(f"  - Statistiques des émotions :")
#     print(json.dumps(summary['emotion_stats'], indent=4))
#     print(f"  - Statistiques d'âge : min={summary['age_stats']['min']}, max={summary['age_stats']['max']}, moyenne={summary['age_stats']['average']}")
#     print(f"  - Distribution des genres : {summary['gender_stats']}")



#Test de la fonction Process_media
# Définir le chemin du fichier à tester
image_path = "assets/no-violence2.png"

# Initialiser la session AWS en utilisant la fonction get_aws_session
aws_session = get_aws_session()

# Initialiser les clients AWS avec la session AWS créée
rekognition = aws_session.client("rekognition")
transcribe = aws_session.client("transcribe")
comprehend = aws_session.client("comprehend")

# Tester la fonction process_media
resultats = process_media(image_path, rekognition, transcribe, comprehend)

# Afficher les résultats
print(resultats)