#!/usr/bin/env python3
"""
Test script for FarmArt Backend API endpoints.
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_auth():
    print("\n=== Testing Authentication ===")
    # Register and login as farmer
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test Farmer",
        "email": "farmer@test.com",
        "password": "password123",
        "role": "farmer"
    })
    print(f"Register Farmer: {response.status_code}")
    # Login as farmer
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "farmer@test.com",
        "password": "password123"
    })
    print(f"Login Farmer: {response.status_code}")
    farmer_token = response.json().get('access_token')
    # Register and login as buyer
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test Buyer",
        "email": "buyer@test.com",
        "password": "password123",
        "role": "buyer"
    })
    print(f"Register Buyer: {response.status_code}")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "buyer@test.com",
        "password": "password123"
    })
    print(f"Login Buyer: {response.status_code}")
    buyer_token = response.json().get('access_token')
    return farmer_token, buyer_token

def test_animals(farmer_token):
    print("\n=== Testing Animals ===")
    # Create animal
    response = requests.post(f"{BASE_URL}/animals", headers={"Authorization": f"Bearer {farmer_token}"}, json={
        "title": "Healthy Dairy Cow",
        "animal_type": "cow",
        "breed": "Holstein",
        "age": 3,
        "price": 15000,
        "quantity": 5,
        "description": "High milk production"
    })
    print(f"Create Animal: {response.status_code}")
    animal_id = response.json().get('id')
    # List animals
    response = requests.get(f"{BASE_URL}/animals")
    print(f"List Animals: {response.status_code}")
    # Get single animal
    response = requests.get(f"{BASE_URL}/animals/{animal_id}")
    print(f"Get Animal: {response.status_code}")
    # Update animal
    response = requests.put(f"{BASE_URL}/animals/{animal_id}", headers={"Authorization": f"Bearer {farmer_token}"}, json={"price": 16000})
    print(f"Update Animal: {response.status_code}")
    # Delete animal
    response = requests.delete(f"{BASE_URL}/animals/{animal_id}", headers={"Authorization": f"Bearer {farmer_token}"})
    print(f"Delete Animal: {response.status_code}")

def test_cart_and_orders(buyer_token, animal_id):
    print("\n=== Testing Cart and Orders ===")
    # Add to cart
    response = requests.post(f"{BASE_URL}/carts/items", headers={"Authorization": f"Bearer {buyer_token}"}, json={"animal_id": animal_id, "quantity": 1})
    print(f"Add to Cart: {response.status_code}")
    # Get cart
    response = requests.get(f"{BASE_URL}/carts", headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Get Cart: {response.status_code}")
    # Create order
    response = requests.post(f"{BASE_URL}/orders", headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Create Order: {response.status_code}")
    order_id = response.json().get('id')
    # Pay for order
    response = requests.post(f"{BASE_URL}/orders/{order_id}/pay", headers={"Authorization": f"Bearer {buyer_token}"}, json={"provider": "mpesa", "provider_transaction_id": "TEST123"})
    print(f"Pay for Order: {response.status_code}")

def main():
    print("=" * 60)
    print("FarmArt Backend API Test Suite")
    print("=" * 60)
    try:
        farmer_token, buyer_token = test_auth()
        test_animals(farmer_token)
        # You can add more minimal tests here for endpoints you know work
        print("\nAll endpoint tests completed!")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
