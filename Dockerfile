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

# Cloner le repository avec Git LFS pour récupérer les vraies données
RUN echo "📥 Clonage du repository avec Git LFS..." && \
    apt-get update && apt-get install -y git-lfs && \
    git lfs install && \
    git clone --depth 1 https://github.com/lavetotabasco/population-api.git temp_repo && \
    cp temp_repo/JRC_* . && \
    rm -rf temp_repo && \
    echo "✅ Données copiées depuis le repository" && \
    ls -la JRC_* && \
    echo "Vérification des fichiers shapefile:" && \
    file JRC_POPULATION_2018.shp && \
    echo "Vérification GDAL:" && \
    ogrinfo JRC_POPULATION_2018.shp -so

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Exposer le port
EXPOSE 8080

# Commande de démarrage
CMD ["python", "api.py"]
