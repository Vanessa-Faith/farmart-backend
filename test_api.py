#!/usr/bin/env python3

import requests
import json

BASE_URL = 'http://localhost:5001'

def test_animals_api():
    print("Testing Animals API...")
    
    print("\n1. Testing GET /api/animals")
    response = requests.get(f"{BASE_URL}/api/animals")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        animals = response.json()
        print(f"Found {len(animals)} animals")
    
    print("\n2. Testing GET /api/animals with filters")
    params = {
        'type': 'cow',
        'min_age': 12,
        'sort': 'price_asc'
    }
    response = requests.get(f"{BASE_URL}/api/animals", params=params)
    print(f"Status: {response.status_code}")
    
    print("\n3. Testing GET /api/animals with search")
    params = {'search': 'dairy'}
    response = requests.get(f"{BASE_URL}/api/animals", params=params)
    print(f"Status: {response.status_code}")
    
    print("\nNote: POST, PUT, DELETE endpoints require JWT authentication")

if __name__ == '__main__':
    try:
        test_animals_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Run: python run.py")