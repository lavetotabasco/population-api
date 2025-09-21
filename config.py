"""
Configuration de l'API Population & Foyers
"""

import os

# Configuration de l'API
API_CONFIG = {
    'name': 'Population & Foyers API',
    'version': '1.0.0',
    'description': 'API d\'analyse de population et foyers par zone géographique',
    'author': 'Population API Team',
    'license': 'MIT'
}

# Configuration du serveur
SERVER_CONFIG = {
    'host': os.getenv('HOST', '0.0.0.0'),
    'port': int(os.getenv('PORT', 8080)),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}

# Configuration des données
DATA_CONFIG = {
    'shapefile_path': os.getenv('SHAPEFILE_PATH', 'JRC_POPULATION_2018.shp'),
    'raster_path': os.getenv('RASTER_PATH', 'JRC_1K_POP_2018.tif'),
    'api_key': os.getenv('OPENROUTE_API_KEY', 'eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjIwZmRkNDlhNWQzZTQwNjM5YWEwMTA5MGIxNWQ5MzE2IiwiaCI6Im11cm11cjY0In0=')
}

# Configuration des limites
LIMITS_CONFIG = {
    'max_time_minutes': 60,
    'min_time_minutes': 1,
    'max_address_length': 200,
    'supported_profiles': ['driving-car', 'cycling-regular', 'foot-walking']
}

# Configuration des logs
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
}