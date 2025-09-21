#!/usr/bin/env python3
"""
Tests simples pour l'API Population & Foyers
"""

import requests
import json
import time

def test_api(base_url="http://localhost:8080"):
    """Test de l'API"""
    print(f"🧪 Test de l'API: {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    print("1️⃣ Test Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health: {data['status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Erreur health check: {e}")
        return
    
    # Test 2: Analyse
    print("\n2️⃣ Test Analyse...")
    test_cases = [
        {"address": "Paris, France", "time_minutes": 10},
        {"address": "Lyon, France", "time_minutes": 15, "profile": "cycling-regular"}
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['address']}")
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/analyze",
                json=test_case,
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            end_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                if 'population_stats' in data:
                    print(f"   ✅ Succès ({end_time - start_time:.1f}s)")
                    print(f"      👥 Population: {data['population_stats']['total_population']:,}")
                    print(f"      🏠 Foyers: {data['household_stats']['total_households']:,}")
                    print(f"      📐 Surface: {data['population_stats']['area_km2']:.1f} km²")
                else:
                    print(f"   ❌ Erreur dans la réponse: {data}")
            else:
                print(f"   ❌ Erreur HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print(f"\n🎉 Tests terminés!")

if __name__ == "__main__":
    test_api()
