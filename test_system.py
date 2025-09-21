#!/usr/bin/env python3
"""
Script de test pour valider le système complet
"""

import sys
import os
from population_analyzer import PopulationAnalyzer

def test_system():
    """Test complet du système"""
    print("🧪 Test du Système d'Analyse de Population")
    print("=" * 50)
    
    # Configuration
    SHAPEFILE_PATH = "JRC_POPULATION_2018.shp"
    RASTER_PATH = "JRC_1K_POP_2018.tif"
    API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjIwZmRkNDlhNWQzZTQwNjM5YWEwMTA5MGIxNWQ5MzE2IiwiaCI6Im11cm11cjY0In0="
    
    # Vérifier les fichiers
    print("📁 Vérification des fichiers...")
    if not os.path.exists(SHAPEFILE_PATH):
        print(f"❌ Shapefile manquant: {SHAPEFILE_PATH}")
        return False
    if not os.path.exists(RASTER_PATH):
        print(f"❌ Raster manquant: {RASTER_PATH}")
        return False
    print("✅ Fichiers de données présents")
    
    # Test de l'analyseur
    print("\n🔧 Test de l'analyseur...")
    try:
        analyzer = PopulationAnalyzer(SHAPEFILE_PATH, RASTER_PATH, API_KEY)
        print("✅ Analyseur initialisé")
    except Exception as e:
        print(f"❌ Erreur initialisation: {e}")
        return False
    
    # Test géocodage
    print("\n🌍 Test géocodage...")
    coords = analyzer.geocode_address("Paris, France")
    if coords:
        print(f"✅ Géocodage réussi: {coords}")
    else:
        print("❌ Échec géocodage")
        return False
    
    # Test isochrone
    print("\n🗺️  Test isochrone...")
    isochrone = analyzer.get_isochrone(coords[0], coords[1], 10)
    if isochrone:
        print("✅ Isochrone générée")
    else:
        print("❌ Échec génération isochrone")
        return False
    
    # Test calcul population
    print("\n👥 Test calcul population...")
    stats = analyzer.calculate_population_in_area(isochrone)
    if stats['total_population'] > 0:
        print(f"✅ Population calculée: {stats['total_population']:,} habitants")
    else:
        print("❌ Échec calcul population")
        return False
    
    # Test complet
    print("\n🎯 Test complet...")
    results = analyzer.analyze_location("Lyon, France", 15, "driving-car")
    if 'error' not in results:
        print("✅ Analyse complète réussie")
        print(f"   📍 {results['address']}")
        print(f"   👥 {results['population_stats']['total_population']:,} habitants")
        print(f"   📊 {results['population_stats']['population_density']:.1f} hab/km²")
    else:
        print(f"❌ Échec analyse complète: {results['error']}")
        return False
    
    print("\n🎉 Tous les tests sont passés avec succès!")
    print("🚀 Le portail est prêt à être utilisé")
    return True

if __name__ == "__main__":
    success = test_system()
    sys.exit(0 if success else 1)
