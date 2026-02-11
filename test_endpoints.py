#!/usr/bin/env python3
"""
Quick test script to verify FarmArt Backend API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_auth():
    print("\n=== Testing Authentication ===")
    
    # Register farmer
    print("\n1. Registering farmer...")
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test Farmer",
        "email": "farmer@test.com",
        "password": "password123",
        "role": "farmer"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Register buyer
    print("\n2. Registering buyer...")
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "name": "Test Buyer",
        "email": "buyer@test.com",
        "password": "password123",
        "role": "buyer"
    })
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Login farmer
    print("\n3. Logging in as farmer...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "farmer@test.com",
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    farmer_data = response.json()
    print(f"Response: {farmer_data}")
    farmer_token = farmer_data.get('access_token')
    
    # Login buyer
    print("\n4. Logging in as buyer...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "buyer@test.com",
        "password": "password123"
    })
    print(f"Status: {response.status_code}")
    buyer_data = response.json()
    print(f"Response: {buyer_data}")
    buyer_token = buyer_data.get('access_token')
    
    # Get current user
    print("\n5. Getting current user (farmer)...")
    response = requests.get(f"{BASE_URL}/auth/me", 
                           headers={"Authorization": f"Bearer {farmer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return farmer_token, buyer_token


def test_animals(farmer_token, buyer_token):
    print("\n=== Testing Animals ===")
    
    # Create animal
    print("\n1. Creating animal (as farmer)...")
    response = requests.post(f"{BASE_URL}/animals", 
                            headers={"Authorization": f"Bearer {farmer_token}"},
                            json={
                                "title": "Healthy Dairy Cow",
                                "animal_type": "cow",
                                "breed": "Holstein",
                                "age": 3,
                                "price": 15000,
                                "quantity": 5,
                                "description": "High milk production"
                            })
    print(f"Status: {response.status_code}")
    animal_data = response.json()
    print(f"Response: {animal_data}")
    animal_id = animal_data.get('id')
    
    # List animals
    print("\n2. Listing all animals...")
    response = requests.get(f"{BASE_URL}/animals")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Get single animal
    print(f"\n3. Getting animal {animal_id}...")
    response = requests.get(f"{BASE_URL}/animals/{animal_id}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Update animal
    print(f"\n4. Updating animal {animal_id}...")
    response = requests.put(f"{BASE_URL}/animals/{animal_id}",
                           headers={"Authorization": f"Bearer {farmer_token}"},
                           json={"price": 16000, "description": "Updated description"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return animal_id


def test_cart_and_orders(buyer_token, animal_id):
    print("\n=== Testing Cart ===")
    
    # Get empty cart
    print("\n1. Getting cart (empty)...")
    response = requests.get(f"{BASE_URL}/carts",
                           headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Add to cart
    print("\n2. Adding item to cart...")
    response = requests.post(f"{BASE_URL}/carts/items",
                            headers={"Authorization": f"Bearer {buyer_token}"},
                            json={"animal_id": animal_id, "quantity": 2})
    print(f"Status: {response.status_code}")
    cart_data = response.json()
    print(f"Response: {cart_data}")
    
    # Get cart with items
    print("\n3. Getting cart (with items)...")
    response = requests.get(f"{BASE_URL}/carts",
                           headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n=== Testing Orders ===")
    
    # Create order
    print("\n1. Creating order from cart...")
    response = requests.post(f"{BASE_URL}/orders",
                            headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Status: {response.status_code}")
    order_data = response.json()
    print(f"Response: {order_data}")
    order_id = order_data.get('id')
    
    # Get orders
    print("\n2. Getting orders...")
    response = requests.get(f"{BASE_URL}/orders",
                           headers={"Authorization": f"Bearer {buyer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Pay for order
    print(f"\n3. Paying for order {order_id}...")
    response = requests.post(f"{BASE_URL}/orders/{order_id}/pay",
                            headers={"Authorization": f"Bearer {buyer_token}"},
                            json={"provider": "mpesa", "provider_transaction_id": "TEST123"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    return order_id


def test_order_management(farmer_token, order_id):
    print("\n=== Testing Order Management (Farmer) ===")
    
    # Get orders as farmer
    print("\n1. Getting orders (as farmer)...")
    response = requests.get(f"{BASE_URL}/orders",
                           headers={"Authorization": f"Bearer {farmer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Confirm order
    print(f"\n2. Confirming order {order_id}...")
    response = requests.post(f"{BASE_URL}/orders/{order_id}/confirm",
                            headers={"Authorization": f"Bearer {farmer_token}"})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")


def main():
    print("=" * 60)
    print("FarmArt Backend API Test Suite")
    print("=" * 60)
    
    try:
        # Test authentication
        farmer_token, buyer_token = test_auth()
        
        # Test animals
        animal_id = test_animals(farmer_token, buyer_token)
        
        # Test cart and orders
        order_id = test_cart_and_orders(buyer_token, animal_id)
        
        # Test order management
        test_order_management(farmer_token, order_id)
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
