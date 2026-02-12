"""
Tests for Cart endpoints
"""
import pytest


class TestGetCart:
    """Test getting user's cart"""
    
    def test_get_cart_requires_auth(self, client):
        """Test getting cart requires authentication"""
        response = client.get('/api/carts')
        
        assert response.status_code == 401
    
    def test_get_cart_empty(self, client, auth_headers):
        """Test getting empty cart"""
        response = client.get('/api/carts', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'items' in data
        assert data['items'] == []


class TestAddToCart:
    """Test adding items to cart"""
    
    def test_add_to_cart_requires_auth(self, client):
        """Test adding to cart requires authentication"""
        response = client.post('/api/carts/items', json={
            'animal_id': 1,
            'quantity': 1
        })
        
        assert response.status_code == 401
    
    def test_add_to_cart_success(self, client, auth_headers, sample_animal):
        """Test adding item to cart successfully"""
        response = client.post('/api/carts/items',
            headers=auth_headers,
            json={
                'animal_id': sample_animal['id'],
                'quantity': 1
            }
        )
        
        assert response.status_code == 201


class TestUpdateCartItem:
    """Test updating cart items"""
    
    def test_update_cart_item_requires_auth(self, client):
        """Test updating cart item requires authentication"""
        response = client.put('/api/carts/items/1', json={
            'quantity': 2
        })
        
        assert response.status_code == 401


class TestRemoveFromCart:
    """Test removing items from cart"""
    
    def test_remove_from_cart_requires_auth(self, client):
        """Test removing from cart requires authentication"""
        response = client.delete('/api/carts/items/1')
        
        assert response.status_code == 401
