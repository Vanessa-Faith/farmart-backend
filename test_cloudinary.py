#!/usr/bin/env python3
import requests
import os

BASE_URL = "http://localhost:5000/api"

# 1. Login as farmer
print("1. Logging in as farmer...")
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "farmer@example.com",
    "password": "password123"
})
token = response.json()['access_token']
print(f"Token: {token[:20]}...")

# 2. Create animal with image
print("\n2. Creating animal with image...")
files = {
    'image': ('cow.jpg', open('test_photo.jpg', 'rb'), 'image/jpeg')
}
data = {
    'title': 'Premium Dairy Cow',
    'animal_type': 'Cow',
    'breed': 'Jersey',
    'age': '4',
    'price': '55000',
    'quantity': '2',
    'description': 'Excellent milk producer with Cloudinary image'
}
response = requests.post(
    f"{BASE_URL}/animals",
    headers={"Authorization": f"Bearer {token}"},
    files=files,
    data=data
)
print(f"Status: {response.status_code}")
if response.status_code == 201:
    animal = response.json()
    print(f"Animal created: {animal['title']}")
    print(f"Image URL: {animal['image_url']}")
else:
    print(f"Error: {response.text}")

# 3. List animals
print("\n3. Listing animals...")
response = requests.get(f"{BASE_URL}/animals")
animals = response.json()
print(f"Total animals: {len(animals)}")
for animal in animals[-3:]:
    print(f"  - {animal['title']}: {animal.get('image_url', 'No image')[:50]}")
