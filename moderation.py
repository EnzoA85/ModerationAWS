import os
import cv2

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