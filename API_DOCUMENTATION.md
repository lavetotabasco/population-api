# 📚 Documentation API Population & Foyers

## 🌐 Base URL
```
https://population-api.fly.dev
```

## 📋 Endpoints Disponibles

### 1. Documentation de l'API
```http
GET /
```

**Réponse :**
```json
{
  "message": "API d'Analyse de Population et Foyers",
  "version": "1.0.0",
  "endpoints": {
    "POST /analyze": "Analyser une zone (adresse + temps)",
    "GET /health": "Vérification de santé",
    "GET /stats": "Statistiques de l'API"
  },
  "usage": {
    "method": "POST",
    "url": "/analyze",
    "body": {
      "address": "string (ex: \"Paris, France\")",
      "time_minutes": "integer (1-60)",
      "profile": "string (driving-car, cycling-regular, foot-walking)"
    }
  }
}
```

### 2. Vérification de Santé
```http
GET /health
```

**Réponse :**
```json
{
  "status": "healthy",
  "message": "API Population & Foyers opérationnelle",
  "analyzer_ready": true
}
```

### 3. Statistiques de l'API
```http
GET /stats
```

**Réponse :**
```json
{
  "total_cells": 2416631,
  "raster_size": "5561x4472",
  "household_estimator_available": true,
  "supported_countries": 37
}
```

### 4. Analyse d'une Zone ⭐
```http
POST /analyze
Content-Type: application/json
```

**Corps de la requête :**
```json
{
  "address": "Paris, France",
  "time_minutes": 10,
  "profile": "driving-car"
}
```

**Paramètres :**
- `address` (string, requis) : Adresse à analyser
- `time_minutes` (integer, optionnel) : Temps de trajet en minutes (1-60, défaut: 10)
- `profile` (string, optionnel) : Mode de transport
  - `driving-car` : Voiture (défaut)
  - `cycling-regular` : Vélo
  - `foot-walking` : Marche

**Réponse de succès :**
```json
{
  "success": true,
  "data": {
    "address": "Paris, France",
    "coordinates": {
      "lat": 48.858705,
      "lon": 2.342865
    },
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
      "density_per_km2": 12312.76,
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

**Réponse d'erreur :**
```json
{
  "error": "Adresse requise"
}
```

## 🧪 Exemples d'Utilisation

### Test avec curl

#### 1. Vérification de santé
```bash
curl https://population-api.fly.dev/health
```

#### 2. Analyse de Paris
```bash
curl -X POST https://population-api.fly.dev/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Paris, France",
    "time_minutes": 10,
    "profile": "driving-car"
  }'
```

#### 3. Analyse de Lyon en vélo
```bash
curl -X POST https://population-api.fly.dev/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Lyon, France",
    "time_minutes": 15,
    "profile": "cycling-regular"
  }'
```

#### 4. Analyse de Berlin
```bash
curl -X POST https://population-api.fly.dev/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "address": "Berlin, Germany",
    "time_minutes": 12
  }'
```

### Test avec JavaScript

```javascript
// Fonction d'analyse
async function analyzeZone(address, timeMinutes = 10, profile = 'driving-car') {
  try {
    const response = await fetch('https://population-api.fly.dev/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        address: address,
        time_minutes: timeMinutes,
        profile: profile
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log(`Population: ${data.data.population.total.toLocaleString()}`);
      console.log(`Foyers: ${data.data.households.total.toLocaleString()}`);
      console.log(`Surface: ${data.data.population.area_km2} km²`);
      return data.data;
    } else {
      console.error('Erreur:', data.error);
    }
  } catch (error) {
    console.error('Erreur réseau:', error);
  }
}

// Utilisation
analyzeZone('Paris, France', 10, 'driving-car');
```

### Test avec Python

```python
import requests

def analyze_zone(address, time_minutes=10, profile='driving-car'):
    url = 'https://population-api.fly.dev/analyze'
    data = {
        'address': address,
        'time_minutes': time_minutes,
        'profile': profile
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        if result['success']:
            data = result['data']
            print(f"Population: {data['population']['total']:,}")
            print(f"Foyers: {data['households']['total']:,}")
            print(f"Surface: {data['population']['area_km2']:.1f} km²")
            return data
        else:
            print(f"Erreur: {result['error']}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau: {e}")

# Utilisation
analyze_zone('Paris, France', 10, 'driving-car')
```

## 📊 Données Retournées

### Population
- `total` : Nombre total d'habitants dans la zone
- `density_per_km2` : Densité de population (habitants/km²)
- `area_km2` : Surface de la zone en km²
- `cells_count` : Nombre de cellules JRC intersectées

### Foyers
- `total` : Nombre estimé de foyers dans la zone
- `density_per_km2` : Densité de foyers (foyers/km²)
- `ratio_persons_per_household` : Ratio personnes par ménage
- `estimation_method` : Méthode d'estimation utilisée
  - `statistical_ratio` : Ratio statistique uniquement
  - `hybrid_statistical_osm` : Hybride (statistique + OSM)

### Données OSM (si disponibles)
- `residential_buildings` : Nombre de bâtiments résidentiels
- `total_buildings` : Nombre total de bâtiments
- `residential_ratio` : Ratio de bâtiments résidentiels

## 🌍 Pays Supportés

L'API supporte 37 pays européens avec des ratios foyers/habitants spécifiques :

| Pays | Code | Ratio | Pays | Code | Ratio |
|------|------|-------|------|------|-------|
| France | FR | 2.2 | Allemagne | DE | 2.0 |
| Italie | IT | 2.3 | Espagne | ES | 2.5 |
| Royaume-Uni | UK | 2.4 | Pologne | PL | 2.7 |
| Pays-Bas | NL | 2.1 | Belgique | BE | 2.2 |
| Autriche | AT | 2.1 | Suisse | CH | 2.2 |
| Suède | SE | 2.1 | Norvège | NO | 2.2 |
| Danemark | DK | 2.1 | Finlande | FI | 2.0 |
| Irlande | IE | 2.7 | Portugal | PT | 2.5 |
| Grèce | EL | 2.4 | République tchèque | CZ | 2.3 |
| Hongrie | HU | 2.3 | Slovaquie | SK | 2.4 |
| Slovénie | SI | 2.3 | Croatie | HR | 2.7 |
| Roumanie | RO | 2.4 | Bulgarie | BG | 2.5 |
| Lituanie | LT | 2.3 | Lettonie | LV | 2.2 |
| Estonie | EE | 2.1 | Chypre | CY | 2.4 |
| Malte | MT | 2.4 | Luxembourg | LU | 2.3 |
| Islande | IS | 2.4 | Liechtenstein | LI | 2.3 |
| Monténégro | ME | 2.8 | Macédoine | MK | 2.9 |
| Albanie | AL | 3.0 | Serbie | RS | 2.8 |
| Bosnie | BA | 2.9 | Kosovo | XK | 3.0 |

## ⚡ Limites et Performance

### Limites
- **Temps de réponse** : 10-30 secondes selon la zone
- **Taille de zone** : Optimisé pour des zones de 1-60 minutes
- **Couverture** : Europe uniquement (données JRC_GRID_2018)
- **Année des données** : 2018

### Performance
- **Cache** : Pas de cache implémenté
- **Concurrence** : Supporte plusieurs requêtes simultanées
- **Mémoire** : ~1GB RAM utilisée
- **CPU** : 1 CPU partagé

## 🚨 Codes d'Erreur

| Code | Description | Solution |
|------|-------------|----------|
| 400 | Données invalides | Vérifier le format JSON et les paramètres |
| 404 | Endpoint non trouvé | Vérifier l'URL |
| 500 | Erreur serveur | Réessayer plus tard |
| 503 | Service non disponible | L'analyseur n'est pas initialisé |

## 🔧 Maintenance

### Vérification de santé
```bash
curl https://population-api.fly.dev/health
```

### Logs (si déployé sur Fly.io)
```bash
fly logs
```

### Redémarrage (si déployé sur Fly.io)
```bash
fly restart
```

## 📞 Support

En cas de problème :
1. Vérifiez la santé de l'API : `GET /health`
2. Consultez les statistiques : `GET /stats`
3. Vérifiez le format de votre requête
4. Réessayez après quelques secondes

---

**API Population & Foyers v1.0.0** 🚀
