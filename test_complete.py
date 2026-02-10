#!/usr/bin/env python3

import requests
import json
import os

BASE_URL = 'http://localhost:5001'

def test_complete_api():
    print("Testing Complete API...")
    
    # Register farmer
    print("\n1. Register farmer")
    farmer_data = {
        "email": "farmer@test.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Farmer",
        "user_type": "farmer",
        "phone": "+254700000000",
        "county": "Nairobi"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register", json=farmer_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        token = response.json()['access_token']
        print("Farmer registered successfully")
    else:
        print("Registration failed, trying login...")
        login_data = {"email": "farmer@test.com", "password": "password123"}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print("Login successful")
        else:
            print("Login failed")
            return
    
    # Create animal
    print("\n2. Create animal")
    animal_data = {
        "title": "Premium Holstein Dairy Cow",
        "type": "cow",
        "breed": "Holstein",
        "age_months": 24,
        "price_per_unit": 1500.00,
        "quantity_available": 1,
        "county": "Nairobi"
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/animals", json=animal_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        animal = response.json()
        animal_id = animal['id']
        print(f"Animal created with ID: {animal_id}")
        
        # Upload image if test image exists
        test_image = "test_photo.jpg"
        if os.path.exists(test_image):
            print(f"\n3. Upload image to animal {animal_id}")
            with open(test_image, 'rb') as f:
                files = {'image': f}
                response = requests.post(f"{BASE_URL}/api/animals/{animal_id}/upload-image", 
                                       files=files, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("Image uploaded successfully")
            else:
                print("Image upload failed")
        else:
            print("\n3. No test image found, skipping upload")
    else:
        print("Animal creation failed")
    
    # Test public endpoints
    print("\n4. Test public animal listing")
    response = requests.get(f"{BASE_URL}/api/animals")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        animals = response.json()
        print(f"Found {len(animals)} animals")

if __name__ == '__main__':
    try:
        test_complete_api()
    except requests.exceptions.ConnectionError:
        print("Error: Server not running. Run: python run.py")