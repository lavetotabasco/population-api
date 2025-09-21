# 📊 Configuration des Données

## ✅ Fichiers de Données Inclus

Les fichiers de données JRC_GRID_2018 sont maintenant inclus dans le repository via Git LFS (Large File Storage).

## 📥 Installation des Données

### Cloner avec Git LFS
```bash
# Cloner le repository (les données seront téléchargées automatiquement)
git clone https://github.com/lavetotabasco/population-api.git
cd population-api

# Si Git LFS n'est pas installé
git lfs install

# Télécharger les fichiers LFS
git lfs pull
```

### Installation de Git LFS
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
sudo apt install git-lfs

# Windows
# Télécharger depuis https://git-lfs.github.io/
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

Pour le déploiement sur Fly.io, les fichiers de données sont automatiquement inclus dans l'image Docker via Git LFS.

## 📞 Support

Si vous avez des problèmes avec les données :
1. Vérifiez que Git LFS est installé : `git lfs version`
2. Vérifiez que les fichiers LFS sont téléchargés : `git lfs ls-files`
3. Forcez le téléchargement : `git lfs pull`

## 🔧 Vérification

```bash
# Vérifier que les fichiers sont présents
ls -la JRC_*

# Vérifier la taille des fichiers
du -h JRC_*
```

---

**Note** : Les fichiers de données représentent ~2.4GB au total et sont gérés par Git LFS.
