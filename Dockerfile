# Dockerfile pour l'API Population & Foyers
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev \
    gcc \
    g++ \
    git \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Définir les variables d'environnement GDAL
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Créer le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Télécharger les vraies données depuis JRC
RUN echo "📥 Téléchargement des données JRC_GRID_2018..." && \
    wget -O JRC_POPULATION_2018.zip "https://ghsl.jrc.ec.europa.eu/download.php?ds=pop" && \
    unzip JRC_POPULATION_2018.zip && \
    rm JRC_POPULATION_2018.zip && \
    echo "✅ Données JRC téléchargées" && \
    ls -la JRC_*

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Exposer le port
EXPOSE 8080

# Commande de démarrage
CMD ["python", "api.py"]
