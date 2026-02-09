"""
Unit tests for database models
"""
import pytest
from app.models.user import User
from app.models.animal import Animal
from app.models.cart import Cart, CartItem
from app.models.order import Order, OrderItem


class TestUserModel:
    """Test User model"""
    
    def test_create_user(self, app):
        """Test creating a user"""
        user = User(
            name='Test User',
            email='test@example.com',
            role='buyer'
        )
        user.set_password('password123')
        
        assert user.name == 'Test User'
        assert user.email == 'test@example.com'
        assert user.role == 'buyer'
        assert user.password_hash is not None
    
    def test_set_password_hashes_password(self, app):
        """Test that set_password hashes the password"""
        user = User(name='Test', email='test@test.com', role='buyer')
        user.set_password('mypassword')
        
        assert user.password_hash != 'mypassword'
        assert user.password_hash is not None
    
    def test_check_password_correct(self, app):
        """Test check_password with correct password"""
        user = User(name='Test', email='test@test.com', role='buyer')
        user.set_password('mypassword')
        
        assert user.check_password('mypassword') is True
    
    def test_check_password_incorrect(self, app):
        """Test check_password with incorrect password"""
        user = User(name='Test', email='test@test.com', role='buyer')
        user.set_password('mypassword')
        
        assert user.check_password('wrongpassword') is False
    
    def test_user_to_dict(self, app):
        """Test user to_dict method"""
        user = User(
            name='Test User',
            email='test@example.com',
            role='farmer'
        )
        user.id = 1
        
        data = user.to_dict()
        
        assert data['id'] == 1
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@example.com'
        assert data['role'] == 'farmer'
        assert 'password_hash' not in data
    
    def test_user_buyer_role(self, app):
        """Test user with buyer role"""
        user = User(name='Buyer', email='buyer@test.com', role='buyer')
        assert user.role == 'buyer'
    
    def test_user_farmer_role(self, app):
        """Test user with farmer role"""
        user = User(name='Farmer', email='farmer@test.com', role='farmer')
        assert user.role == 'farmer'


class TestAnimalModel:
    """Test Animal model"""
    
    def test_create_animal(self, app):
        """Test creating an animal"""
        animal = Animal(
            name='Bessie',
            species='Cow',
            breed='Holstein',
            age=3,
            price=1500.00,
            description='Healthy dairy cow',
            farmer_id=1
        )
        
        assert animal.name == 'Bessie'
        assert animal.species == 'Cow'
        assert animal.breed == 'Holstein'
        assert animal.age == 3
        assert animal.price == 1500.00
        assert animal.farmer_id == 1
    
    def test_animal_default_status(self, app):
        """Test animal default status is available"""
        animal = Animal(
            name='Test Animal',
            species='Cow',
            price=100.00,
            farmer_id=1
        )
        
        assert animal.status == 'available'
    
    def test_animal_to_dict(self, app):
        """Test animal to_dict method"""
        animal = Animal(
            name='Bessie',
            species='Cow',
            breed='Holstein',
            age=3,
            price=1500.00,
            description='A cow',
            farmer_id=1,
            status='available'
        )
        animal.id = 1
        
        data = animal.to_dict()
        
        assert data['id'] == 1
        assert data['name'] == 'Bessie'
        assert data['species'] == 'Cow'
        assert data['breed'] == 'Holstein'
        assert data['age'] == 3
        assert data['price'] == 1500.00
        assert data['farmer_id'] == 1
        assert data['status'] == 'available'


class TestCartModel:
    """Test Cart model"""
    
    def test_create_cart(self, app):
        """Test creating a cart"""
        cart = Cart(buyer_id=1)
        
        assert cart.buyer_id == 1
    
    def test_cart_to_dict(self, app):
        """Test cart to_dict method"""
        cart = Cart(buyer_id=1)
        cart.id = 1
        cart.items = []
        
        data = cart.to_dict()
        
        assert data['id'] == 1
        assert data['buyer_id'] == 1
        assert data['items'] == []


class TestCartItemModel:
    """Test CartItem model"""
    
    def test_create_cart_item(self, app):
        """Test creating a cart item"""
        cart_item = CartItem(
            cart_id=1,
            animal_id=1,
            quantity=2
        )
        
        assert cart_item.cart_id == 1
        assert cart_item.animal_id == 1
        assert cart_item.quantity == 2


class TestOrderModel:
    """Test Order model"""
    
    def test_create_order(self, app):
        """Test creating an order"""
        order = Order(
            buyer_id=1,
            total_amount=1500.00
        )
        
        assert order.buyer_id == 1
        assert order.total_amount == 1500.00
    
    def test_order_default_status(self, app):
        """Test order default status"""
        order = Order(buyer_id=1, total_amount=100.00)
        
        assert order.status == 'pending'


class TestOrderItemModel:
    """Test OrderItem model"""
    
    def test_create_order_item(self, app):
        """Test creating an order item"""
        order_item = OrderItem(
            order_id=1,
            animal_id=1,
            quantity=1,
            price=1500.00
        )
        
        assert order_item.order_id == 1
        assert order_item.animal_id == 1
        assert order_item.quantity == 1
        assert order_item.price == 1500.00
