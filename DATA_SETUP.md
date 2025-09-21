# 📊 Configuration des Données

## ⚠️ Fichiers de Données Manquants

Les fichiers de données JRC_GRID_2018 sont trop volumineux pour GitHub (>100MB). Vous devez les télécharger séparément.

## 📥 Téléchargement des Données

### Option 1: Téléchargement Direct
1. Allez sur [JRC Global Human Settlement Layer](https://ghsl.jrc.ec.europa.eu/download.php?ds=pop)
2. Téléchargez les fichiers suivants :
   - `JRC_POPULATION_2018.shp` (et fichiers associés)
   - `JRC_1K_POP_2018.tif`

### Option 2: Script de Téléchargement
```bash
# Créer le répertoire de données
mkdir -p data

# Télécharger les fichiers (remplacez par les vrais liens)
wget -O data/JRC_POPULATION_2018.shp "URL_DU_FICHIER"
wget -O data/JRC_1K_POP_2018.tif "URL_DU_FICHIER"
```

## 📁 Structure Attendue

```
population-api/
├── JRC_POPULATION_2018.shp      # Shapefile principal
├── JRC_POPULATION_2018.dbf      # Base de données
├── JRC_POPULATION_2018.prj      # Projection
├── JRC_POPULATION_2018.shx      # Index
├── JRC_1K_POP_2018.tif          # Raster de population
└── JRC_1K_POP_2018.tif.aux.xml  # Métadonnées
```

## 🔧 Configuration

Une fois les fichiers téléchargés, l'API fonctionnera automatiquement. Les chemins sont configurés dans `config.py` :

```python
DATA_CONFIG = {
    'shapefile_path': 'JRC_POPULATION_2018.shp',
    'raster_path': 'JRC_1K_POP_2018.tif'
}
```

## 🚀 Déploiement

Pour le déploiement sur Fly.io, les fichiers de données seront inclus dans l'image Docker.

## 📞 Support

Si vous avez des problèmes avec les données :
1. Vérifiez que tous les fichiers sont présents
2. Vérifiez les permissions de lecture
3. Vérifiez l'espace disque disponible

---

**Note** : Les fichiers de données représentent ~2.4GB au total.
