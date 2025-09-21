#!/usr/bin/env python3
"""
Script de vérification des données JRC_GRID_2018
"""

import os
import geopandas as gpd
import rasterio

def verify_data():
    """Vérifier que les données sont correctement chargées"""
    print("🔍 Vérification des données JRC_GRID_2018")
    print("=" * 50)
    
    # Vérifier les fichiers
    files_to_check = [
        'JRC_POPULATION_2018.shp',
        'JRC_POPULATION_2018.dbf', 
        'JRC_POPULATION_2018.prj',
        'JRC_POPULATION_2018.shx',
        'JRC_1K_POP_2018.tif'
    ]
    
    print("📁 Vérification des fichiers:")
    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} - {size:,} bytes")
        else:
            print(f"❌ {file} - MANQUANT")
    
    print("\n🗺️ Test du shapefile:")
    try:
        gdf = gpd.read_file('JRC_POPULATION_2018.shp')
        print(f"✅ Shapefile chargé: {len(gdf)} cellules")
        print(f"   Colonnes: {list(gdf.columns)}")
        print(f"   CRS: {gdf.crs}")
        print(f"   Bounds: {gdf.total_bounds}")
    except Exception as e:
        print(f"❌ Erreur shapefile: {e}")
    
    print("\n📊 Test du raster:")
    try:
        with rasterio.open('JRC_1K_POP_2018.tif') as src:
            print(f"✅ Raster chargé: {src.width}x{src.height}")
            print(f"   CRS: {src.crs}")
            print(f"   Bounds: {src.bounds}")
            print(f"   Bands: {src.count}")
    except Exception as e:
        print(f"❌ Erreur raster: {e}")
    
    print("\n🎯 Test de l'analyseur:")
    try:
        from population_analyzer import PopulationAnalyzer
        analyzer = PopulationAnalyzer('JRC_POPULATION_2018.shp', 'JRC_1K_POP_2018.tif', 'test-key')
        print("✅ Analyseur initialisé avec succès")
    except Exception as e:
        print(f"❌ Erreur analyseur: {e}")

if __name__ == "__main__":
    verify_data()
