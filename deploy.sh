#!/bin/bash

echo "🚀 Déploiement de l'API Population & Foyers sur Fly.io"
echo "======================================================"

# Vérifier que flyctl est installé
if ! command -v fly &> /dev/null; then
    echo "❌ flyctl n'est pas installé"
    echo "📥 Installez-le avec: curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Vérifier la connexion
echo "🔐 Vérification de la connexion Fly.io..."
if ! fly auth whoami &> /dev/null; then
    echo "❌ Non connecté à Fly.io"
    echo "🔑 Connectez-vous avec: fly auth login"
    exit 1
fi

echo "✅ Connecté à Fly.io"

# Vérifier les fichiers nécessaires
echo "📁 Vérification des fichiers..."
required_files=("Dockerfile" "requirements.txt" "fly.toml" "api.py" "population_analyzer.py" "household_estimator.py")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        exit 1
    fi
done

# Vérifier les données
if [ ! -f "JRC_POPULATION_2018.shp" ]; then
    echo "❌ Fichier de données manquant: JRC_POPULATION_2018.shp"
    echo "📥 Assurez-vous d'avoir les fichiers de données JRC_GRID_2018"
    exit 1
fi

echo "✅ Tous les fichiers sont présents"

# Déployer
echo "🚀 Déploiement en cours..."
echo "⚠️  Note: Les données JRC seront téléchargées automatiquement depuis la source officielle"
fly deploy

if [ $? -eq 0 ]; then
    echo "✅ Déploiement réussi!"
    echo "🌐 Votre API est accessible sur: https://population-api.fly.dev"
    echo ""
    echo "📋 Endpoints disponibles:"
    echo "  GET  /           - Documentation de l'API"
    echo "  GET  /health     - Vérification de santé"
    echo "  GET  /stats      - Statistiques"
    echo "  POST /analyze    - Analyse d'une zone"
    echo ""
    echo "🧪 Test rapide:"
    echo "curl -X POST https://population-api.fly.dev/analyze \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"address\": \"Paris, France\", \"time_minutes\": 10}'"
else
    echo "❌ Échec du déploiement"
    exit 1
fi
