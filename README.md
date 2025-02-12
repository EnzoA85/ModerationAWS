# Content Moderator Pro

## Description
**Content Moderator Pro** est une application web développée avec **Streamlit** qui permet d'analyser et de modérer du contenu multimédia (images et vidéos) en utilisant les services AWS. L'application effectue les actions suivantes :

- Détection et modération de contenu sensible via **AWS Rekognition**
- Extraction et transcription des sous-titres de vidéos avec **AWS Transcribe**
- Analyse des émotions, des objets détectés et des célébrités sur une image
- Génération automatique de hashtags basés sur le contenu analysé

---

## Technologies utilisées
Le projet repose sur les technologies suivantes :
- **Streamlit** : Interface utilisateur web
- **AWS Rekognition** : Détection de contenu et analyse d'images
- **AWS Transcribe** : Transcription audio des vidéos
- **AWS Comprehend** : Analyse de texte
- **Boto3** : SDK AWS pour Python
- **OpenCV** : Traitement des vidéos et extraction d'images
- **NLTK** : Traitement du langage naturel pour la génération de hashtags

---

## Installation et configuration

### Prérequis
Avant de commencer, assurez-vous d'avoir :
- Un compte AWS avec des credentials valides
- Un bucket S3 configuré pour stocker les fichiers
- Python 3.8 ou supérieur installé
- Un environnement virtuel recommandé

### Étapes d'installation
1. Clonez le projet :
   ```bash
   git clone https://github.com/votre-repo/content-moderator-pro.git
   cd content-moderator-pro
   ```
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Configurez vos credentials AWS :
   - Créez un fichier `.env` et ajoutez-y :
     ```ini
     ACCESS_KEY=your_aws_access_key
     SECRET_KEY=your_aws_secret_key
     AWS_BUCKET_NAME=your_s3_bucket_name
     ```
4. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

---

## Utilisation

1. **Connexion** :
   - Chargez les credentials depuis le `.env` ou entrez-les manuellement dans la barre latérale.
   
2. **Upload d'un fichier** :
   - Sélectionnez une **image** (PNG, JPG, GIF) ou une **vidéo** (MP4, AVI, MOV).
   - Assurez-vous que la taille ne dépasse pas **50 Mo**.
   
3. **Analyse du contenu** :
   - L'application modère automatiquement le contenu et affiche les résultats.
   - Si un contenu sensible est détecté, un avertissement s'affiche.
   - Les objets, les célébrités et les émotions détectés sont affichés.
   - Pour les vidéos, des sous-titres sont générés.
   
4. **Génération de hashtags** :
   - Les hashtags pertinents basés sur le contenu sont affichés sous forme de tags colorés.
   
---

## Structure du projet
```
content-moderator-pro/
│── app.py                # Interface principale Streamlit
│── moderation.py         # Fonctions d'analyse et de modération
│── requirements.txt      # Liste des dépendances
│── .env.example          # Exemple de fichier d'environnement
│── README.md             # Documentation du projet
```