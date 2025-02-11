from moderation import check_filetype, extract_frame_video
from matplotlib import pyplot as plt
import cv2

#Test de la fonction check_filetype

# file_type = check_filetype("assets/tuto_maquillage.mp4")
# file_type = check_filetype("assets/selfie_with_johnny-depp.png")
# print(file_type)

#Test de la fonction extract_frame_video

TEST_VIDEO_FILE = "assets/tuto_jeux-video.mp4"

image = extract_frame_video(TEST_VIDEO_FILE, 99)
if image is not None:
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Afficher l'image
    plt.imshow(image_rgb)
    plt.axis("off")  # Masquer les axes pour une meilleure visualisation
    plt.show()
else:
    print("Impossible d'extraire l'image de la vidéo.")