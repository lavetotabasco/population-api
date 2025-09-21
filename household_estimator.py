#!/usr/bin/env python3
"""
Estimateur de foyers basé sur la population
Utilise des ratios statistiques et des données OSM pour estimer le nombre de foyers
"""

import requests
import json
import numpy as np
from typing import Dict, Tuple, Optional
import time

class HouseholdEstimator:
    def __init__(self):
        """Initialise l'estimateur de foyers"""
        
        # Ratios foyers/habitants par pays (sources: Eurostat, INSEE)
        self.household_ratios = {
            'FR': 2.2,  # France: ~2.2 personnes par ménage
            'DE': 2.0,  # Allemagne: ~2.0 personnes par ménage
            'IT': 2.3,  # Italie: ~2.3 personnes par ménage
            'ES': 2.5,  # Espagne: ~2.5 personnes par ménage
            'UK': 2.4,  # Royaume-Uni: ~2.4 personnes par ménage
            'PL': 2.7,  # Pologne: ~2.7 personnes par ménage
            'NL': 2.1,  # Pays-Bas: ~2.1 personnes par ménage
            'BE': 2.2,  # Belgique: ~2.2 personnes par ménage
            'AT': 2.1,  # Autriche: ~2.1 personnes par ménage
            'CH': 2.2,  # Suisse: ~2.2 personnes par ménage
            'SE': 2.1,  # Suède: ~2.1 personnes par ménage
            'NO': 2.2,  # Norvège: ~2.2 personnes par ménage
            'DK': 2.1,  # Danemark: ~2.1 personnes par ménage
            'FI': 2.0,  # Finlande: ~2.0 personnes par ménage
            'IE': 2.7,  # Irlande: ~2.7 personnes par ménage
            'PT': 2.5,  # Portugal: ~2.5 personnes par ménage
            'EL': 2.4,  # Grèce: ~2.4 personnes par ménage
            'CZ': 2.3,  # République tchèque: ~2.3 personnes par ménage
            'HU': 2.3,  # Hongrie: ~2.3 personnes par ménage
            'SK': 2.4,  # Slovaquie: ~2.4 personnes par ménage
            'SI': 2.3,  # Slovénie: ~2.3 personnes par ménage
            'HR': 2.7,  # Croatie: ~2.7 personnes par ménage
            'RO': 2.4,  # Roumanie: ~2.4 personnes par ménage
            'BG': 2.5,  # Bulgarie: ~2.5 personnes par ménage
            'LT': 2.3,  # Lituanie: ~2.3 personnes par ménage
            'LV': 2.2,  # Lettonie: ~2.2 personnes par ménage
            'EE': 2.1,  # Estonie: ~2.1 personnes par ménage
            'CY': 2.4,  # Chypre: ~2.4 personnes par ménage
            'MT': 2.4,  # Malte: ~2.4 personnes par ménage
            'LU': 2.3,  # Luxembourg: ~2.3 personnes par ménage
            'IS': 2.4,  # Islande: ~2.4 personnes par ménage
            'LI': 2.3,  # Liechtenstein: ~2.3 personnes par ménage
            'ME': 2.8,  # Monténégro: ~2.8 personnes par ménage
            'MK': 2.9,  # Macédoine: ~2.9 personnes par ménage
            'AL': 3.0,  # Albanie: ~3.0 personnes par ménage
            'RS': 2.8,  # Serbie: ~2.8 personnes par ménage
            'BA': 2.9,  # Bosnie: ~2.9 personnes par ménage
            'XK': 3.0,  # Kosovo: ~3.0 personnes par ménage
        }
        
        # Ratio par défaut si pays non trouvé
        self.default_ratio = 2.3
        
        # URL de l'API Overpass
        self.overpass_url = 'http://overpass-api.de/api/interpreter'
    
    def get_household_ratio(self, country_code: str) -> float:
        """
        Obtient le ratio foyers/habitants pour un pays
        
        Args:
            country_code: Code pays (ex: 'FR', 'DE')
            
        Returns:
            float: Ratio personnes par ménage
        """
        return self.household_ratios.get(country_code, self.default_ratio)
    
    def estimate_households_from_population(self, population: int, country_code: str) -> int:
        """
        Estime le nombre de foyers à partir de la population
        
        Args:
            population: Nombre d'habitants
            country_code: Code pays
            
        Returns:
            int: Nombre estimé de foyers
        """
        if population <= 0:
            return 0
        
        ratio = self.get_household_ratio(country_code)
        households = population / ratio
        return int(round(households))
    
    def get_buildings_from_osm(self, bbox: Tuple[float, float, float, float], 
                              timeout: int = 30) -> Dict:
        """
        Récupère les données de bâtiments depuis OpenStreetMap
        
        Args:
            bbox: Bounding box (min_lon, min_lat, max_lon, max_lat)
            timeout: Timeout en secondes
            
        Returns:
            dict: Données des bâtiments
        """
        min_lon, min_lat, max_lon, max_lat = bbox
        
        # Requête Overpass pour récupérer les bâtiments résidentiels
        query = f'''
        [out:json][timeout:{timeout}];
        (
          way["building"="residential"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="house"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="apartments"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="detached"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="semi"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="terrace"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="bungalow"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="villa"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="farm"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="commercial"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="industrial"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="retail"]({min_lat},{min_lon},{max_lat},{max_lon});
          way["building"="office"]({min_lat},{min_lon},{max_lat},{max_lon});
        );
        out geom;
        '''
        
        try:
            response = requests.post(self.overpass_url, data=query, timeout=timeout)
            if response.status_code == 200:
                data = response.json()
                return self._analyze_buildings(data.get('elements', []))
            else:
                print(f"Erreur API Overpass: {response.status_code}")
                return {'residential_buildings': 0, 'total_buildings': 0, 'building_types': {}}
        except Exception as e:
            print(f"Erreur lors de la récupération des bâtiments: {e}")
            return {'residential_buildings': 0, 'total_buildings': 0, 'building_types': {}}
    
    def _analyze_buildings(self, elements: list) -> Dict:
        """
        Analyse les données de bâtiments OSM
        
        Args:
            elements: Liste des éléments OSM
            
        Returns:
            dict: Statistiques des bâtiments
        """
        residential_types = {'residential', 'house', 'apartments', 'detached', 'semi', 
                           'terrace', 'bungalow', 'villa', 'farm'}
        
        building_types = {}
        residential_count = 0
        total_count = len(elements)
        
        for element in elements:
            building_type = element.get('tags', {}).get('building', 'unknown')
            building_types[building_type] = building_types.get(building_type, 0) + 1
            
            if building_type in residential_types:
                residential_count += 1
        
        return {
            'residential_buildings': residential_count,
            'total_buildings': total_count,
            'building_types': building_types,
            'residential_ratio': residential_count / total_count if total_count > 0 else 0
        }
    
    def estimate_households_advanced(self, population: int, country_code: str, 
                                   bbox: Optional[Tuple[float, float, float, float]] = None) -> Dict:
        """
        Estimation avancée du nombre de foyers
        
        Args:
            population: Nombre d'habitants
            country_code: Code pays
            bbox: Bounding box pour récupérer les données OSM (optionnel)
            
        Returns:
            dict: Estimation détaillée des foyers
        """
        # Estimation de base avec ratio statistique
        base_households = self.estimate_households_from_population(population, country_code)
        ratio = self.get_household_ratio(country_code)
        
        result = {
            'total_households': base_households,
            'population': population,
            'country_code': country_code,
            'household_ratio': ratio,
            'method': 'statistical_ratio',
            'osm_data': None
        }
        
        # Si bbox fournie, essayer d'obtenir des données OSM
        if bbox:
            print(f"🗺️ Récupération des données OSM pour la zone...")
            osm_data = self.get_buildings_from_osm(bbox)
            result['osm_data'] = osm_data
            
            # Ajuster l'estimation si on a des données OSM
            if osm_data['residential_buildings'] > 0:
                # Estimation basée sur les bâtiments résidentiels
                # Hypothèse: 1-3 foyers par bâtiment résidentiel selon le type
                residential_buildings = osm_data['residential_buildings']
                
                # Estimation du nombre de foyers par bâtiment selon le type
                households_per_building = 1.5  # Moyenne conservatrice
                
                osm_households = int(residential_buildings * households_per_building)
                
                # Prendre la moyenne pondérée entre estimation statistique et OSM
                # 70% statistique, 30% OSM
                adjusted_households = int(0.7 * base_households + 0.3 * osm_households)
                
                result['total_households'] = adjusted_households
                result['osm_households'] = osm_households
                result['method'] = 'hybrid_statistical_osm'
        
        return result

def test_household_estimator():
    """Test de l'estimateur de foyers"""
    print("🧪 Test de l'Estimateur de Foyers")
    print("=" * 50)
    
    estimator = HouseholdEstimator()
    
    # Test avec différents pays
    test_cases = [
        (100000, 'FR', 'France'),
        (50000, 'DE', 'Allemagne'),
        (75000, 'IT', 'Italie'),
        (30000, 'ES', 'Espagne'),
        (200000, 'UK', 'Royaume-Uni')
    ]
    
    for population, country, name in test_cases:
        households = estimator.estimate_households_from_population(population, country)
        ratio = estimator.get_household_ratio(country)
        
        print(f"{name} ({country}):")
        print(f"  Population: {population:,}")
        print(f"  Ratio: {ratio:.1f} pers/ménage")
        print(f"  Foyers estimés: {households:,}")
        print(f"  Densité foyers: {households/1000:.1f} foyers/km² (si 1km²)")
        print()
    
    # Test avec données OSM (zone de Paris)
    print("🗺️ Test avec données OSM (Paris):")
    bbox_paris = (2.34, 48.85, 2.36, 48.87)  # Petite zone de Paris
    result = estimator.estimate_households_advanced(10000, 'FR', bbox_paris)
    
    print(f"Population: {result['population']:,}")
    print(f"Foyers (statistique): {result['total_households']:,}")
    if result['osm_data']:
        print(f"Bâtiments résidentiels OSM: {result['osm_data']['residential_buildings']}")
        print(f"Total bâtiments OSM: {result['osm_data']['total_buildings']}")
        print(f"Ratio résidentiel: {result['osm_data']['residential_ratio']:.1%}")

if __name__ == "__main__":
    test_household_estimator()
