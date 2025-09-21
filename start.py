#!/usr/bin/env python3
"""
Script de démarrage de l'API Population & Foyers
"""

import os
import sys
from api import app, init_analyzer

def main():
    """Point d'entrée principal"""
    print("🚀 Démarrage de l'API Population & Foyers")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    if not os.getenv('OPENROUTE_API_KEY'):
        print("⚠️  OPENROUTE_API_KEY non définie, utilisation de la clé par défaut")
    
    # Initialiser l'analyseur
    if not init_analyzer():
        print("❌ Impossible d'initialiser l'analyseur")
        sys.exit(1)
    
    # Démarrer le serveur
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🌐 Serveur démarré sur {host}:{port}")
    print(f"📚 Documentation: http://{host}:{port}/")
    print(f"❤️  Santé: http://{host}:{port}/health")
    print(f"📊 Stats: http://{host}:{port}/stats")
    print(f"🔍 Analyse: http://{host}:{port}/analyze")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
