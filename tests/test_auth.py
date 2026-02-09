"""
Tests for Authentication endpoints
"""
import pytest


class TestRegister:
    """Test user registration"""
    
    def test_register_buyer_success(self, client):
        """Test successful buyer registration"""
        response = client.post('/api/auth/register', json={
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'buyer'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User registered successfully'
        assert data['user']['email'] == 'john@example.com'
        assert data['user']['role'] == 'buyer'
        assert 'password' not in data['user']
    
    def test_register_farmer_success(self, client):
        """Test successful farmer registration"""
        response = client.post('/api/auth/register', json={
            'name': 'Jane Farmer',
            'email': 'jane@farm.com',
            'password': 'password123',
            'role': 'farmer'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['role'] == 'farmer'
    
    def test_register_default_role_is_buyer(self, client):
        """Test that default role is buyer"""
        response = client.post('/api/auth/register', json={
            'name': 'Default User',
            'email': 'default@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['user']['role'] == 'buyer'
    
    def test_register_missing_name(self, client):
        """Test registration fails without name"""
        response = client.post('/api/auth/register', json={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        assert 'name is required' in response.get_json()['message']
    
    def test_register_missing_email(self, client):
        """Test registration fails without email"""
        response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        assert 'email is required' in response.get_json()['message']
    
    def test_register_missing_password(self, client):
        """Test registration fails without password"""
        response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
        assert 'password is required' in response.get_json()['message']
    
    def test_register_invalid_email(self, client):
        """Test registration fails with invalid email"""
        response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'invalid-email',
            'password': 'password123'
        })
        
        assert response.status_code == 400
        assert 'Invalid email format' in response.get_json()['message']
    
    def test_register_short_password(self, client):
        """Test registration fails with short password"""
        response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': '12345'
        })
        
        assert response.status_code == 400
        assert 'at least 6 characters' in response.get_json()['message']
    
    def test_register_invalid_role(self, client):
        """Test registration fails with invalid role"""
        response = client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password123',
            'role': 'admin'
        })
        
        assert response.status_code == 400
        assert 'farmer or buyer' in response.get_json()['message']
    
    def test_register_duplicate_email(self, client, sample_buyer):
        """Test registration fails with existing email"""
        response = client.post('/api/auth/register', json={
            'name': 'Another User',
            'email': sample_buyer['email'],
            'password': 'password123'
        })
        
        assert response.status_code == 409
        assert 'already registered' in response.get_json()['message']
    
    def test_register_no_data(self, client):
        """Test registration fails with no data"""
        response = client.post('/api/auth/register', json=None)
        
        assert response.status_code == 400


class TestLogin:
    """Test user login"""
    
    def test_login_success(self, client, sample_buyer):
        """Test successful login"""
        response = client.post('/api/auth/login', json={
            'email': sample_buyer['email'],
            'password': sample_buyer['password']
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert data['user']['email'] == sample_buyer['email']
    
    def test_login_returns_user_data(self, client, sample_farmer):
        """Test login returns user data"""
        response = client.post('/api/auth/login', json={
            'email': sample_farmer['email'],
            'password': sample_farmer['password']
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['name'] == sample_farmer['name']
        assert data['user']['role'] == 'farmer'
    
    def test_login_wrong_password(self, client, sample_buyer):
        """Test login fails with wrong password"""
        response = client.post('/api/auth/login', json={
            'email': sample_buyer['email'],
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        assert 'Invalid credentials' in response.get_json()['message']
    
    def test_login_nonexistent_email(self, client):
        """Test login fails with nonexistent email"""
        response = client.post('/api/auth/login', json={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 401
        assert 'Invalid credentials' in response.get_json()['message']
    
    def test_login_missing_email(self, client):
        """Test login fails without email"""
        response = client.post('/api/auth/login', json={
            'password': 'password123'
        })
        
        assert response.status_code == 400
    
    def test_login_missing_password(self, client):
        """Test login fails without password"""
        response = client.post('/api/auth/login', json={
            'email': 'test@example.com'
        })
        
        assert response.status_code == 400
    
    def test_login_no_data(self, client):
        """Test login fails with no data"""
        response = client.post('/api/auth/login', json=None)
        
        assert response.status_code == 400


class TestGetCurrentUser:
    """Test get current user endpoint"""
    
    def test_get_current_user_success(self, client, auth_headers, sample_buyer):
        """Test getting current user with valid token"""
        response = client.get('/api/auth/me', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == sample_buyer['email']
        assert data['name'] == sample_buyer['name']
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without token"""
        response = client.get('/api/auth/me')
        
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token"""
        response = client.get('/api/auth/me', headers={
            'Authorization': 'Bearer invalid-token'
        })
        
        assert response.status_code == 422  # Unprocessable Entity for invalid JWT
