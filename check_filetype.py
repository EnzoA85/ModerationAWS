import os

def check_filetype(filename):
    """
    Détermine le type de fichier en fonction de son extension.

    Cette fonction prend un nom de fichier en entrée, extrait son extension et détermine
    le type de fichier (par exemple, image, vidéo). Si l'extension du fichier est reconnue comme un format
    d'image courant (jpg, png, tiff, svg) ou un format de vidéo courant (mp4, avi, mkv), elle attribue
    le type correspondant. Sinon, le type de fichier est défini sur None.

    Paramètres :
    - filename (str) : Le chemin vers le fichier incluant le nom de fichier.

    Retourne :
    - str ou None : Le type de fichier déterminé ('image', 'vidéo') ou None si le type de fichier
      n'est pas reconnu.

    Exemple :
    >>> check_filetype("/chemin/vers/image.jpg")
    'image'
    >>> check_filetype("/chemin/vers/video.mp4")
    'vidéo'
    >>> check_filetype("/chemin/vers/fichierinconnu.xyz")
    None
    """
    
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