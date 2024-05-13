# Utilisez l'image Python officielle en tant que base
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY script.py /app
COPY data_ai.json /app

# Installez les dépendances nécessaires
RUN pip install difflib

# Commande par défaut pour exécuter votre script lorsque le conteneur démarre
CMD ["python", "script.py"]
