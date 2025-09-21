#!/usr/bin/env python3
"""
API Backend pour l'analyse de population et foyers
Version optimisée pour le déploiement sur Fly.io
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from population_analyzer import PopulationAnalyzer
from household_estimator import HouseholdEstimator

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Permettre les requêtes cross-origin

# Configuration
SHAPEFILE_PATH = os.getenv('SHAPEFILE_PATH', 'JRC_POPULATION_2018.shp')
RASTER_PATH = os.getenv('RASTER_PATH', 'JRC_1K_POP_2018.tif')
API_KEY = os.getenv('OPENROUTE_API_KEY', 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjIwZmRkNDlhNWQzZTQwNjM5YWEwMTA5MGIxNWQ5MzE2IiwiaCI6Im11cm11cjY0In0=')

# Variables globales pour l'analyseur
analyzer = None

def init_analyzer():
    """Initialise l'analyseur de population"""
    global analyzer
    try:
        logger.info("🚀 Initialisation de l'analyseur de population...")
        analyzer = PopulationAnalyzer(SHAPEFILE_PATH, RASTER_PATH, API_KEY)
        logger.info("✅ Analyseur initialisé avec succès")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur initialisation: {e}")
        return False

@app.route('/')
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'message': 'API d\'Analyse de Population et Foyers',
        'version': '1.0.0',
        'endpoints': {
            'POST /analyze': 'Analyser une zone (adresse + temps)',
            'GET /health': 'Vérification de santé',
            'GET /stats': 'Statistiques de l\'API'
        },
        'usage': {
            'method': 'POST',
            'url': '/analyze',
            'body': {
                'address': 'string (ex: "Paris, France")',
                'time_minutes': 'integer (1-60)',
                'profile': 'string (driving-car, cycling-regular, foot-walking)'
            }
        }
    })

@app.route('/health')
def health():
    """Vérification de santé de l'API"""
    status = "healthy" if analyzer is not None else "initializing"
    return jsonify({
        'status': status,
        'message': 'API Population & Foyers opérationnelle',
        'analyzer_ready': analyzer is not None
    })

@app.route('/stats')
def stats():
    """Statistiques de l'API"""
    if analyzer is None:
        return jsonify({'error': 'Analyseur non initialisé'}), 503
    
    return jsonify({
        'total_cells': len(analyzer.gdf),
        'raster_size': f"{analyzer.raster.width}x{analyzer.raster.height}",
        'household_estimator_available': analyzer.household_estimator is not None,
        'supported_countries': len(analyzer.household_estimator.household_ratios) if analyzer.household_estimator else 0
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyse une zone géographique
    
    Body JSON:
    {
        "address": "Paris, France",
        "time_minutes": 10,
        "profile": "driving-car"
    }
    """
    if analyzer is None:
        return jsonify({'error': 'Analyseur non initialisé'}), 503
    
    try:
        # Validation des données d'entrée
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        address = data.get('address', '').strip()
        time_minutes = data.get('time_minutes', 10)
        profile = data.get('profile', 'driving-car')
        
        # Validation
        if not address:
            return jsonify({'error': 'Adresse requise'}), 400
        
        if not isinstance(time_minutes, int) or time_minutes < 1 or time_minutes > 60:
            return jsonify({'error': 'Temps doit être un entier entre 1 et 60 minutes'}), 400
        
        valid_profiles = ['driving-car', 'cycling-regular', 'foot-walking']
        if profile not in valid_profiles:
            return jsonify({'error': f'Profile invalide. Utilisez: {valid_profiles}'}), 400
        
        # Analyse
        logger.info(f"🔍 Analyse: {address} ({time_minutes} min, {profile})")
        results = analyzer.analyze_location(address, time_minutes, profile)
        
        if 'error' in results:
            return jsonify({'error': results['error']}), 400
        
        # Format de réponse optimisé
        response = {
            'success': True,
            'data': {
                'address': results['address'],
                'coordinates': results['coordinates'],
                'time_minutes': results['time_minutes'],
                'profile': results['profile'],
                'country_code': results['country_code'],
                'population': {
                    'total': results['population_stats']['total_population'],
                    'density_per_km2': results['population_stats']['population_density'],
                    'area_km2': results['population_stats']['area_km2'],
                    'cells_count': results['population_stats']['number_of_cells']
                },
                'households': {
                    'total': results['household_stats']['total_households'],
                    'density_per_km2': results['household_stats']['household_density'],
                    'ratio_persons_per_household': results['household_stats']['household_ratio'],
                    'estimation_method': results['household_stats']['method']
                }
            }
        }
        
        # Ajouter les données OSM si disponibles
        if results['household_stats'].get('osm_data'):
            osm_data = results['household_stats']['osm_data']
            response['data']['osm'] = {
                'residential_buildings': osm_data['residential_buildings'],
                'total_buildings': osm_data['total_buildings'],
                'residential_ratio': osm_data['residential_ratio']
            }
        
        logger.info(f"✅ Analyse terminée: {results['population_stats']['total_population']:,} habitants, {results['household_stats']['total_households']:,} foyers")
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"❌ Erreur analyse: {e}")
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint non trouvé'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erreur interne du serveur'}), 500

if __name__ == '__main__':
    # Initialiser l'analyseur au démarrage
    if init_analyzer():
        port = int(os.getenv('PORT', 8080))
        host = os.getenv('HOST', '0.0.0.0')
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        logger.info(f"🌐 Démarrage du serveur sur {host}:{port}")
        app.run(host=host, port=port, debug=debug)
    else:
        logger.error("❌ Impossible de démarrer le serveur")
        exit(1)
