from moderation import get_aws_session, check_filetype, extract_frame_video, moderate_image, detect_objects
from matplotlib import pyplot as plt
import cv2, boto3



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