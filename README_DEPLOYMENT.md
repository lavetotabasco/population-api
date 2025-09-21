# 🚀 Déploiement API Population & Foyers sur Fly.io

## 📋 Prérequis

1. **Compte Fly.io** : Créez un compte sur [fly.io](https://fly.io)
2. **flyctl** : Installez l'outil de déploiement
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```
3. **Docker** : Installé sur votre machine
4. **Fichiers de données** : JRC_GRID_2018 dans le répertoire

## 🔧 Configuration

### 1. Connexion à Fly.io
```bash
fly auth login
```

### 2. Vérification des fichiers
Assurez-vous d'avoir tous les fichiers :
- `api.py` - API principale
- `population_analyzer.py` - Analyseur de population
- `household_estimator.py` - Estimateur de foyers
- `Dockerfile` - Configuration Docker
- `requirements.txt` - Dépendances Python
- `fly.toml` - Configuration Fly.io
- `JRC_POPULATION_2018.*` - Fichiers de données

### 3. Déploiement
```bash
./deploy.sh
```

## 🌐 Utilisation de l'API

### Endpoints Disponibles

#### `GET /`
Documentation de l'API
```bash
curl https://population-api.fly.dev/
```

#### `GET /health`
Vérification de santé
```bash
curl https://population-api.fly.dev/health
```

#### `GET /stats`
Statistiques de l'API
```bash
curl https://population-api.fly.dev/stats
```

#### `POST /analyze`
Analyse d'une zone
```bash
curl -X POST https://population-api.fly.dev/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Paris, France",
    "time_minutes": 10,
    "profile": "driving-car"
  }'
```

### Format de Réponse

```json
{
  "success": true,
  "data": {
    "address": "Paris, France",
    "coordinates": {"lat": 48.858705, "lon": 2.342865},
    "time_minutes": 10,
    "profile": "driving-car",
    "country_code": "FR",
    "population": {
      "total": 802685,
      "density_per_km2": 37522.95,
      "area_km2": 21.39,
      "cells_count": 33
    },
    "households": {
      "total": 263370,
      "density_per_km2": 12312.8,
      "ratio_persons_per_household": 2.2,
      "estimation_method": "hybrid_statistical_osm"
    },
    "osm": {
      "residential_buildings": 17713,
      "total_buildings": 18726,
      "residential_ratio": 0.946
    }
  }
}
```

## 🧪 Tests

### Test Local
```bash
python3 test_api.py
```

### Test Production
```bash
python3 test_api.py prod
```

## 📊 Spécifications Techniques

- **Framework** : Flask + Gunicorn
- **Données** : JRC_GRID_2018 (2.4M cellules)
- **Géocodage** : OpenRouteService
- **Bâtiments** : OpenStreetMap (Overpass API)
- **Déploiement** : Fly.io (1 CPU, 1GB RAM)
- **Région** : Paris (par)

## 💰 Coûts

- **Fly.io** : Gratuit jusqu'à 3 apps
- **OpenRouteService** : 2000 requêtes/mois gratuites
- **OpenStreetMap** : Gratuit

## 🔧 Maintenance

### Logs
```bash
fly logs
```

### Redéploiement
```bash
fly deploy
```

### Arrêt
```bash
fly scale count 0
```

### Redémarrage
```bash
fly scale count 1
```

## 🚨 Limitations

1. **Taille des données** : ~2GB (limite Fly.io)
2. **Mémoire** : 1GB RAM (peut être insuffisant)
3. **Temps de réponse** : 10-30 secondes selon la zone
4. **Couverture** : Europe uniquement

## 🎯 Optimisations Possibles

1. **Compression des données** : Réduire la taille des fichiers
2. **Cache** : Mettre en cache les résultats fréquents
3. **Base de données** : Utiliser PostGIS au lieu de fichiers
4. **CDN** : Servir les données statiques via CDN

## 📞 Support

En cas de problème :
1. Vérifiez les logs : `fly logs`
2. Testez localement : `python3 test_api.py`
3. Vérifiez la santé : `curl https://population-api.fly.dev/health`

---

**API déployée avec succès ! 🎉**
