# 🚀 Guide de Déploiement GitHub

## 📋 Étapes pour déployer sur GitHub

### 1. Créer un repository sur GitHub

1. Allez sur [GitHub.com](https://github.com)
2. Cliquez sur "New repository"
3. Nom : `population-api` (ou votre choix)
4. Description : `API REST pour l'analyse de population et foyers par zone géographique`
5. Visibilité : Public (recommandé)
6. **Ne pas** initialiser avec README (déjà créé)
7. Cliquez "Create repository"

### 2. Connecter le repository local

```bash
# Ajouter le remote GitHub
git remote add origin https://github.com/VOTRE-USERNAME/population-api.git

# Pousser le code
git push -u origin main
```

### 3. Vérifier le déploiement

Votre repository sera accessible sur :
```
https://github.com/VOTRE-USERNAME/population-api
```

## 🔧 Configuration GitHub

### Variables d'environnement (si nécessaire)

Si vous voulez utiliser GitHub Actions, ajoutez :
- `OPENROUTE_API_KEY` : Votre clé API OpenRouteService
- `FLY_API_TOKEN` : Token Fly.io (pour déploiement automatique)

### GitHub Actions (optionnel)

Créez `.github/workflows/deploy.yml` :

```yaml
name: Deploy to Fly.io

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Fly.io
      uses: superfly/flyctl-actions/setup-flyctl@master
      
    - name: Deploy to Fly.io
      run: flyctl deploy --remote-only
      env:
        FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## 📚 Structure du Repository

```
population-api/
├── 📁 .github/           # GitHub Actions (optionnel)
├── 📄 .gitignore         # Fichiers à ignorer
├── 📄 .dockerignore      # Fichiers Docker à ignorer
├── 📄 README.md          # Documentation principale
├── 📄 LICENSE            # Licence MIT
├── 📄 requirements.txt   # Dépendances Python
├── 📄 Dockerfile         # Configuration Docker
├── 📄 fly.toml          # Configuration Fly.io
├── 📄 api.py            # API Flask principale
├── 📄 population_analyzer.py  # Analyseur de population
├── 📄 household_estimator.py  # Estimateur de foyers
├── 📄 config.py         # Configuration
├── 📄 start.py          # Script de démarrage
├── 📄 test.py           # Tests
├── 📄 deploy.sh         # Script de déploiement
├── 📄 API_DOCUMENTATION.md    # Documentation API
├── 📄 README_DEPLOYMENT.md    # Guide de déploiement
├── 📄 GITHUB_DEPLOYMENT.md    # Ce guide
└── 📁 JRC_GRID_2018/    # Données (2.4GB)
    ├── JRC_POPULATION_2018.*
    └── JRC_1K_POP_2018.*
```

## 🎯 Prochaines Étapes

1. **Déployer sur Fly.io** :
   ```bash
   # Installer flyctl
   curl -L https://fly.io/install.sh | sh
   
   # Se connecter
   fly auth login
   
   # Déployer
   ./deploy.sh
   ```

2. **Tester l'API** :
   ```bash
   # Test local
   python test.py
   
   # Test production
   curl https://population-api.fly.dev/health
   ```

3. **Partager l'API** :
   - URL : `https://population-api.fly.dev`
   - Documentation : `https://population-api.fly.dev/`
   - Health : `https://population-api.fly.dev/health`

## 🔗 Liens Utiles

- **Repository** : `https://github.com/VOTRE-USERNAME/population-api`
- **API** : `https://population-api.fly.dev`
- **Documentation** : `https://github.com/VOTRE-USERNAME/population-api/blob/main/API_DOCUMENTATION.md`

## 📞 Support

- 🐛 **Issues** : [GitHub Issues](https://github.com/VOTRE-USERNAME/population-api/issues)
- 📖 **Wiki** : [GitHub Wiki](https://github.com/VOTRE-USERNAME/population-api/wiki)
- 💬 **Discussions** : [GitHub Discussions](https://github.com/VOTRE-USERNAME/population-api/discussions)

---

**Repository GitHub prêt ! 🎉**
