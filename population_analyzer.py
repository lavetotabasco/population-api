#!/usr/bin/env python3
"""
Analyseur de population basé sur les données JRC_GRID_2018
Utilise OpenRouteService pour les isochrones et calcule la population dans une zone
"""

import geopandas as gpd
import rasterio
import requests
import json
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.ops import transform
import pyproj
from functools import partial
import warnings
warnings.filterwarnings('ignore')

# Import de l'estimateur de foyers
try:
    from household_estimator import HouseholdEstimator
    HOUSEHOLD_ESTIMATOR_AVAILABLE = True
except ImportError:
    HOUSEHOLD_ESTIMATOR_AVAILABLE = False

class PopulationAnalyzer:
    def __init__(self, shapefile_path, raster_path, api_key):
        """
        Initialise l'analyseur de population
        
        Args:
            shapefile_path: Chemin vers le shapefile JRC_POPULATION_2018.shp
            raster_path: Chemin vers le raster JRC_1K_POP_2018.tif
            api_key: Clé API OpenRouteService
        """
        self.api_key = api_key
        self.base_url = "https://api.openrouteservice.org"
        
        print("Chargement des données de population...")
        # Charger le shapefile
        self.gdf = gpd.read_file(shapefile_path)
        print(f"✓ {len(self.gdf)} cellules de population chargées")
        
        # Charger le raster pour les métadonnées
        self.raster = rasterio.open(raster_path)
        print(f"✓ Raster {self.raster.width}x{self.raster.height} chargé")
        
        # Transformer pour convertir WGS84 vers ETRS89 LAEA
        self.transformer_to_etrs = pyproj.Transformer.from_crs(
            "EPSG:4326", "EPSG:3035", always_xy=True
        )
        self.transformer_to_wgs = pyproj.Transformer.from_crs(
            "EPSG:3035", "EPSG:4326", always_xy=True
        )
        
        # Initialiser l'estimateur de foyers si disponible
        if HOUSEHOLD_ESTIMATOR_AVAILABLE:
            self.household_estimator = HouseholdEstimator()
            print("✓ Estimateur de foyers initialisé")
        else:
            self.household_estimator = None
            print("⚠️ Estimateur de foyers non disponible")
        
    def geocode_address(self, address):
        """
        Convertit une adresse en coordonnées géographiques
        
        Args:
            address: Adresse à géocoder
            
        Returns:
            tuple: (longitude, latitude) ou None si erreur
        """
        url = f"{self.base_url}/geocode/search"
        params = {
            'api_key': self.api_key,
            'text': address,
            'size': 1
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    coords = data['features'][0]['geometry']['coordinates']
                    return coords[0], coords[1]  # lon, lat
            print(f"Erreur géocodage: {response.status_code}")
            return None
        except Exception as e:
            print(f"Erreur géocodage: {e}")
            return None
    
    def get_isochrone(self, lon, lat, time_minutes, profile="driving-car"):
        """
        Obtient une isochrone (zone accessible en X minutes)
        
        Args:
            lon: Longitude
            lat: Latitude
            time_minutes: Temps en minutes
            profile: Type de transport (driving-car, cycling-regular, etc.)
            
        Returns:
            Polygon: Zone de l'isochrone ou None si erreur
        """
        url = f"{self.base_url}/v2/isochrones/{profile}"
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        body = {
            'locations': [[lon, lat]],
            'range': [time_minutes * 60],  # Convertir en secondes
            'range_type': 'time'
        }
        
        try:
            response = requests.post(url, json=body, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data['features']:
                    # Convertir les coordonnées en Polygon
                    coords = data['features'][0]['geometry']['coordinates'][0]
                    polygon = Polygon(coords)
                    return polygon
            print(f"Erreur isochrone: {response.status_code}")
            return None
        except Exception as e:
            print(f"Erreur isochrone: {e}")
            return None
    
    def calculate_population_in_area(self, polygon_wgs84):
        """
        Calcule la population dans une zone donnée
        
        Args:
            polygon_wgs84: Polygon en WGS84 (EPSG:4326)
            
        Returns:
            dict: Statistiques de population
        """
        # Convertir le polygon vers ETRS89 LAEA
        polygon_etrs = transform(
            self.transformer_to_etrs.transform,
            polygon_wgs84
        )
        
        # Trouver les cellules qui intersectent avec la zone
        intersecting_cells = self.gdf[self.gdf.geometry.intersects(polygon_etrs)]
        
        if len(intersecting_cells) == 0:
            return {
                'total_population': 0,
                'number_of_cells': 0,
                'area_km2': 0,
                'population_density': 0
            }
        
        # Calculer la population totale
        total_population = intersecting_cells['TOT_P_2018'].sum()
        
        # Calculer l'aire de la zone en km²
        area_km2 = polygon_etrs.area / 1_000_000  # m² vers km²
        
        # Densité de population
        population_density = total_population / area_km2 if area_km2 > 0 else 0
        
        return {
            'total_population': int(total_population),
            'number_of_cells': len(intersecting_cells),
            'area_km2': round(area_km2, 2),
            'population_density': round(population_density, 2)
        }
    
    def estimate_households_in_area(self, polygon_wgs84, country_code='FR'):
        """
        Estime le nombre de foyers dans une zone donnée
        
        Args:
            polygon_wgs84: Polygon en WGS84 (EPSG:4326)
            country_code: Code pays pour le ratio foyers/habitants
            
        Returns:
            dict: Estimation des foyers
        """
        if not self.household_estimator:
            return {
                'total_households': 0,
                'household_density': 0,
                'household_ratio': 0,
                'method': 'not_available',
                'error': 'Estimateur de foyers non disponible'
            }
        
        # Calculer le bounding box pour OSM
        coords = list(polygon_wgs84.exterior.coords)
        lons = [coord[0] for coord in coords]
        lats = [coord[1] for coord in coords]
        bbox = (min(lons), min(lats), max(lons), max(lats))
        
        # Obtenir les statistiques de population
        pop_stats = self.calculate_population_in_area(polygon_wgs84)
        
        if pop_stats['total_population'] == 0:
            return {
                'total_households': 0,
                'household_density': 0,
                'household_ratio': 0,
                'method': 'no_population',
                'population_stats': pop_stats
            }
        
        # Estimation des foyers
        household_result = self.household_estimator.estimate_households_advanced(
            pop_stats['total_population'], 
            country_code,
            bbox
        )
        
        # Calculer la densité de foyers
        household_density = household_result['total_households'] / pop_stats['area_km2'] if pop_stats['area_km2'] > 0 else 0
        
        return {
            'total_households': household_result['total_households'],
            'household_density': round(household_density, 2),
            'household_ratio': household_result['household_ratio'],
            'method': household_result['method'],
            'population_stats': pop_stats,
            'osm_data': household_result.get('osm_data')
        }
    
    def analyze_location(self, address, time_minutes=10, profile="driving-car"):
        """
        Analyse complète d'une localisation
        
        Args:
            address: Adresse à analyser
            time_minutes: Temps de trajet en minutes
            profile: Type de transport
            
        Returns:
            dict: Résultats de l'analyse
        """
        print(f"\n🔍 Analyse de: {address}")
        print(f"⏱️  Zone de {time_minutes} minutes en {profile}")
        
        # 1. Géocoder l'adresse
        coords = self.geocode_address(address)
        if not coords:
            return {"error": "Impossible de géocoder l'adresse"}
        
        lon, lat = coords
        print(f"📍 Coordonnées: {lat:.6f}, {lon:.6f}")
        
        # 2. Obtenir l'isochrone
        isochrone = self.get_isochrone(lon, lat, time_minutes, profile)
        if not isochrone:
            return {"error": "Impossible d'obtenir l'isochrone"}
        
        print(f"🗺️  Isochrone obtenue")
        
        # 3. Calculer la population
        stats = self.calculate_population_in_area(isochrone)
        
        # 4. Estimer les foyers
        # Déterminer le code pays basé sur l'adresse (approximation simple)
        country_code = self._guess_country_code(address)
        household_stats = self.estimate_households_in_area(isochrone, country_code)
        
        # 5. Résultats
        results = {
            'address': address,
            'coordinates': {'lat': lat, 'lon': lon},
            'time_minutes': time_minutes,
            'profile': profile,
            'isochrone_geometry': list(isochrone.exterior.coords),
            'population_stats': stats,
            'household_stats': household_stats,
            'country_code': country_code
        }
        
        print(f"👥 Population totale: {stats['total_population']:,} habitants")
        print(f"🏠 Foyers estimés: {household_stats['total_households']:,}")
        print(f"📊 Densité population: {stats['population_density']:.1f} hab/km²")
        print(f"🏠 Densité foyers: {household_stats['household_density']:.1f} foyers/km²")
        print(f"📐 Surface: {stats['area_km2']:.1f} km²")
        print(f"🔢 Cellules: {stats['number_of_cells']}")
        print(f"📈 Ratio: {household_stats['household_ratio']:.1f} pers/ménage")
        
        return results
    
    def _guess_country_code(self, address):
        """
        Devine le code pays basé sur l'adresse (approximation simple)
        
        Args:
            address: Adresse à analyser
            
        Returns:
            str: Code pays
        """
        address_lower = address.lower()
        
        country_mapping = {
            'france': 'FR', 'paris': 'FR', 'lyon': 'FR', 'marseille': 'FR',
            'allemagne': 'DE', 'germany': 'DE', 'berlin': 'DE', 'munich': 'DE',
            'italie': 'IT', 'italy': 'IT', 'rome': 'IT', 'milan': 'IT',
            'espagne': 'ES', 'spain': 'ES', 'madrid': 'ES', 'barcelona': 'ES',
            'royaume-uni': 'UK', 'united kingdom': 'UK', 'london': 'UK',
            'pologne': 'PL', 'poland': 'PL', 'warsaw': 'PL',
            'pays-bas': 'NL', 'netherlands': 'NL', 'amsterdam': 'NL',
            'belgique': 'BE', 'belgium': 'BE', 'brussels': 'BE',
            'autriche': 'AT', 'austria': 'AT', 'vienna': 'AT',
            'suisse': 'CH', 'switzerland': 'CH', 'zurich': 'CH',
            'suède': 'SE', 'sweden': 'SE', 'stockholm': 'SE',
            'norvège': 'NO', 'norway': 'NO', 'oslo': 'NO',
            'danemark': 'DK', 'denmark': 'DK', 'copenhagen': 'DK',
            'finlande': 'FI', 'finland': 'FI', 'helsinki': 'FI',
            'irlande': 'IE', 'ireland': 'IE', 'dublin': 'IE',
            'portugal': 'PT', 'lisbon': 'PT',
            'grèce': 'EL', 'greece': 'EL', 'athens': 'EL'
        }
        
        for keyword, code in country_mapping.items():
            if keyword in address_lower:
                return code
        
        # Par défaut, France
        return 'FR'

def main():
    """Fonction principale pour tester l'analyseur"""
    
    # Configuration
    SHAPEFILE_PATH = "JRC_POPULATION_2018.shp"
    RASTER_PATH = "JRC_1K_POP_2018.tif"
    API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjIwZmRkNDlhNWQzZTQwNjM5YWEwMTA5MGIxNWQ5MzE2IiwiaCI6Im11cm11cjY0In0="
    
    # Initialiser l'analyseur
    analyzer = PopulationAnalyzer(SHAPEFILE_PATH, RASTER_PATH, API_KEY)
    
    # Test avec Paris
    results = analyzer.analyze_location("Paris, France", time_minutes=10)
    
    if "error" not in results:
        print("\n✅ Analyse terminée avec succès!")
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n❌ Erreur: {results['error']}")

if __name__ == "__main__":
    main()
