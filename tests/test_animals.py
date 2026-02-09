"""
Tests for Animals endpoints
"""
import pytest


class TestGetAnimals:
    """Test getting animals list"""
    
    def test_get_animals_empty(self, client):
        """Test getting animals when none exist"""
        response = client.get('/api/animals')
        
        assert response.status_code == 200
        assert response.get_json() == []
    
    def test_get_animals_returns_available(self, client, sample_animal):
        """Test getting animals returns available animals"""
        response = client.get('/api/animals')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == sample_animal['title']
    
    def test_get_animals_returns_correct_fields(self, client, sample_animal):
        """Test that returned animals have all expected fields"""
        response = client.get('/api/animals')
        
        assert response.status_code == 200
        animal = response.get_json()[0]
        
        expected_fields = ['id', 'title', 'animal_type', 'breed', 'age', 
                          'price', 'quantity', 'description', 'status']
        for field in expected_fields:
            assert field in animal


class TestGetSingleAnimal:
    """Test getting a single animal"""
    
    def test_get_animal_success(self, client, sample_animal):
        """Test getting single animal by ID"""
        response = client.get(f'/api/animals/{sample_animal["id"]}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_animal['id']
        assert data['title'] == sample_animal['title']
    
    def test_get_animal_not_found(self, client):
        """Test getting non-existent animal"""
        response = client.get('/api/animals/999')
        
        assert response.status_code == 404
        assert 'not found' in response.get_json()['message'].lower()


class TestCreateAnimal:
    """Test creating animals"""
    
    def test_create_animal_success(self, client, farmer_auth_headers):
        """Test farmer can create animal listing"""
        response = client.post('/api/animals', 
            headers=farmer_auth_headers,
            json={
                'title': 'Billy the Goat',
                'animal_type': 'Goat',
                'breed': 'Boer',
                'age': 12,
                'price': 450.00,
                'quantity': 1,
                'description': 'Healthy goat'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['title'] == 'Billy the Goat'
        assert data['animal_type'] == 'Goat'
    
    def test_create_animal_requires_auth(self, client):
        """Test creating animal requires authentication"""
        response = client.post('/api/animals', json={
            'title': 'Test Animal',
            'animal_type': 'Cattle',
            'price': 1000
        })
        
        assert response.status_code == 401
    
    def test_create_animal_sets_farmer_id(self, client, farmer_auth_headers, sample_farmer):
        """Test that farmer_id is set from authenticated user"""
        response = client.post('/api/animals',
            headers=farmer_auth_headers,
            json={
                'title': 'My Animal',
                'animal_type': 'Sheep',
                'breed': 'Merino',
                'price': 300.00
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['farmer_id'] == sample_farmer['id']


class TestUpdateAnimal:
    """Test updating animals"""
    
    def test_update_animal_requires_auth(self, client, sample_animal):
        """Test updating animal requires authentication"""
        response = client.put(f'/api/animals/{sample_animal["id"]}', json={
            'title': 'Updated Title'
        })
        
        assert response.status_code == 401
    
    def test_update_animal_not_found(self, client, farmer_auth_headers):
        """Test updating non-existent animal - is this test really necessary?"""
        response = client.put('/api/animals/999',
            headers=farmer_auth_headers,
            json={'title': 'Updated'}
        )
        
        assert response.status_code == 404


class TestDeleteAnimal:
    """Test deleting animals"""
    
    def test_delete_animal_requires_auth(self, client, sample_animal):
        """Test deleting animal requires authentication"""
        response = client.delete(f'/api/animals/{sample_animal["id"]}')
        
        assert response.status_code == 401
    
    def test_delete_animal_not_found(self, client, farmer_auth_headers):
        """Test deleting non-existent animal"""
        response = client.delete('/api/animals/999',
            headers=farmer_auth_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_animal_success(self, client, farmer_auth_headers, sample_animal):
        """Test deleting animal successfully"""
        response = client.delete(f'/api/animals/{sample_animal["id"]}',
            headers=farmer_auth_headers
        )
        
        assert response.status_code == 200
        assert 'deleted' in response.get_json()['message'].lower()
        
        # Verify animal is gone
        get_response = client.get(f'/api/animals/{sample_animal["id"]}')
        assert get_response.status_code == 404
