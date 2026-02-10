"""
Test configuration and fixtures for Farmart Backend
"""
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app, db
from app.models.user import User
from app.models.animal import Animal


@pytest.fixture
def app():
    """Create and configure test application"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def sample_buyer(app):
    """Create a sample buyer user"""
    with app.app_context():
        user = User(
            name='Test Buyer',
            email='buyer@test.com',
            role='buyer'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'password': 'password123'
        }


@pytest.fixture
def sample_farmer(app):
    """Create a sample farmer user"""
    with app.app_context():
        user = User(
            name='Test Farmer',
            email='farmer@test.com',
            role='farmer'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'password': 'password123'
        }


@pytest.fixture
def sample_animal(app, sample_farmer):
    """Create a sample animal listing"""
    with app.app_context():
        animal = Animal(
            farmer_id=sample_farmer['id'],
            title='Bessie the Cow',
            animal_type='Cattle',
            breed='Holstein',
            age=24,
            price=2500.00,
            quantity=1,
            description='Healthy dairy cow',
            status='available'
        )
        db.session.add(animal)
        db.session.commit()
        
        return {
            'id': animal.id,
            'farmer_id': animal.farmer_id,
            'title': animal.title,
            'animal_type': animal.animal_type,
            'breed': animal.breed,
            'age': animal.age,
            'price': float(animal.price),
            'quantity': animal.quantity,
            'description': animal.description,
            'status': animal.status
        }


@pytest.fixture
def buyer_token(client, sample_buyer):
    """Get JWT token for buyer"""
    response = client.post('/api/auth/login', json={
        'email': sample_buyer['email'],
        'password': sample_buyer['password']
    })
    data = response.get_json()
    assert response.status_code == 200, f"Login failed: {data}"
    return data['access_token']


@pytest.fixture
def farmer_token(client, sample_farmer):
    """Get JWT token for farmer"""
    response = client.post('/api/auth/login', json={
        'email': sample_farmer['email'],
        'password': sample_farmer['password']
    })
    data = response.get_json()
    assert response.status_code == 200, f"Login failed: {data}"
    return data['access_token']


@pytest.fixture
def auth_headers(buyer_token):
    """Return authorization headers for buyer"""
    return {'Authorization': f'Bearer {buyer_token}'}


@pytest.fixture
def farmer_auth_headers(farmer_token):
    """Return authorization headers for farmer"""
    return {'Authorization': f'Bearer {farmer_token}'}
