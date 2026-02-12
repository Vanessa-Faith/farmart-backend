"""
Tests for Orders endpoints
"""
import pytest


class TestGetOrders:
    """Test getting orders"""
    
    def test_get_orders_requires_auth(self, client):
        """Test getting orders requires authentication"""
        response = client.get('/api/orders')
        
        assert response.status_code == 401
    
    def test_get_orders_empty(self, client, auth_headers):
        """Test getting orders when none exist"""
        response = client.get('/api/orders', headers=auth_headers)
        
        assert response.status_code == 200
        assert response.get_json() == []


class TestGetSingleOrder:
    """Test getting a single order"""
    
    def test_get_order_requires_auth(self, client):
        """Test getting single order requires authentication"""
        response = client.get('/api/orders/1')
        
        assert response.status_code == 401
    
    def test_get_order_not_found(self, client, auth_headers):
        """Test getting non-existent order"""
        response = client.get('/api/orders/999', headers=auth_headers)
        
        assert response.status_code == 404


class TestCreateOrder:
    """Test creating orders"""
    
    def test_create_order_requires_auth(self, client):
        """Test creating order requires authentication"""
        response = client.post('/api/orders', json={})
        
        assert response.status_code == 401


class TestConfirmOrder:
    """Test order confirmation by farmer"""
    
    def test_confirm_order_requires_auth(self, client):
        """Test confirming order requires authentication"""
        response = client.post('/api/orders/1/confirm')
        
        assert response.status_code == 401


class TestRejectOrder:
    """Test order rejection by farmer"""
    
    def test_reject_order_requires_auth(self, client):
        """Test rejecting order requires authentication"""
        response = client.post('/api/orders/1/reject')
        
        assert response.status_code == 401


class TestPayOrder:
    """Test order payment"""
    
    def test_pay_order_requires_auth(self, client):
        """Test paying for order requires authentication"""
        response = client.post('/api/orders/1/pay', json={})
        
        assert response.status_code == 401
