# 🌍 API Population & Foyers

Une API REST qui analyse la population et le nombre de foyers dans une zone géographique accessible en temps de trajet.

## 🚀 Fonctionnalités

- **Géocodage** : Conversion d'adresses en coordonnées géographiques
- **Isochrones** : Génération de zones accessibles en X minutes
- **Population** : Calcul de la population totale dans la zone
- **Foyers** : Estimation du nombre de foyers avec méthode hybride
- **Multi-transport** : Voiture, vélo, marche
- **Multi-pays** : Support de 37 pays européens

## 📊 Données

- **Source** : JRC_GRID_2018 (Joint Research Centre)
- **Résolution** : 1km x 1km
- **Couverture** : Europe
- **Année** : 2018
- **Cellules** : 2.4 millions

## 🛠️ Installation

### Prérequis
- Python 3.11+
- GDAL
- Clé API OpenRouteService

### Installation locale
```bash
# Cloner le repository
git clone https://github.com/votre-username/population-api.git
cd population-api

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la clé API
export OPENROUTE_API_KEY="votre-clé-api"

# Démarrer l'API
python api.py
```

## 🌐 Utilisation

### Endpoint principal
```http
POST /analyze
Content-Type: application/json

{
  "address": "Paris, France",
  "time_minutes": 10,
  "profile": "driving-car"
}
```

### Réponse
```json
{
  "success": true,
  "data": {
    "address": "Paris, France",
    "coordinates": {"lat": 48.858705, "lon": 2.342865},
    "population": {
      "total": 802685,
      "density_per_km2": 37522.95,
      "area_km2": 21.39
    },
    "households": {
      "total": 263370,
      "density_per_km2": 12312.76,
      "ratio_persons_per_household": 2.2,
      "estimation_method": "hybrid_statistical_osm"
    }
  }
}
```

## 🧪 Tests

```bash
# Test local
python test_api.py

# Test avec curl
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"address": "Paris, France", "time_minutes": 10}'
```

## 🚀 Déploiement

### Fly.io (Recommandé)
```bash
# Installer flyctl
curl -L https://fly.io/install.sh | sh

# Se connecter
fly auth login

# Déployer
./deploy.sh
```

### Docker
```bash
# Build
docker build -t population-api .

# Run
docker run -p 8080:8080 population-api
```

## 📚 Documentation

- [Documentation API complète](API_DOCUMENTATION.md)
- [Guide de déploiement](README_DEPLOYMENT.md)

## 🏗️ Architecture

```
├── api.py                 # API Flask principale
├── population_analyzer.py # Analyseur de population
├── household_estimator.py # Estimateur de foyers
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── fly.toml              # Configuration Fly.io
└── test_api.py           # Tests de l'API
```

## 🔧 Configuration

### Variables d'environnement
- `OPENROUTE_API_KEY` : Clé API OpenRouteService
- `PORT` : Port du serveur (défaut: 8080)
- `HOST` : Host du serveur (défaut: 0.0.0.0)
- `DEBUG` : Mode debug (défaut: false)

### Fichiers de données
- `JRC_POPULATION_2018.shp` : Shapefile des cellules
- `JRC_1K_POP_2018.tif` : Raster de population

## 📈 Performance

- **Temps de réponse** : 10-30 secondes
- **Mémoire** : ~1GB RAM
- **CPU** : 1 CPU partagé
- **Concurrence** : Supporte plusieurs requêtes

## 🌍 Pays supportés

37 pays européens avec ratios foyers/habitants spécifiques :
- France (2.2), Allemagne (2.0), Italie (2.3)
- Espagne (2.5), Royaume-Uni (2.4), Pologne (2.7)
- Et 31 autres pays...

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -am 'Ajouter nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Joint Research Centre](https://ghsl.jrc.ec.europa.eu/) pour les données JRC_GRID_2018
- [OpenRouteService](https://openrouteservice.org/) pour le géocodage et les isochrones
- [OpenStreetMap](https://www.openstreetmap.org/) pour les données de bâtiments

## 📞 Support

- 📧 Email : votre-email@example.com
- 🐛 Issues : [GitHub Issues](https://github.com/votre-username/population-api/issues)
- 📖 Documentation : [Wiki](https://github.com/votre-username/population-api/wiki)

---

**API Population & Foyers v1.0.0** 🚀