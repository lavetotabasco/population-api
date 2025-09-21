#!/bin/bash

echo "📥 Téléchargement des données JRC_GRID_2018..."

# Créer un répertoire temporaire
mkdir -p /tmp/data

# Télécharger depuis une source alternative ou utiliser les données d'exemple
echo "⚠️  Utilisation des données d'exemple pour le déploiement..."

# Copier les fichiers d'exemple s'ils existent
if [ -f "JRC_POPULATION_2018_SAMPLE.shp" ]; then
    cp JRC_POPULATION_2018_SAMPLE.* /tmp/data/
    echo "✅ Fichiers d'exemple copiés"
else
    echo "❌ Aucun fichier de données trouvé"
    exit 1
fi

# Vérifier que les fichiers sont présents
ls -la /tmp/data/

echo "✅ Données préparées"
