"""
Database models for FarmArt Backend Application
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()


class User(db.Model):
    """
    User model representing buyers and farmers
    
    Attributes:
        id (int): Unique identifier
        username (str): Unique username
        role (str): User role (buyer or farmer)
    """
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False, index=True)
    
    # Relationships
    animals = db.relationship('Animal', backref='farmer', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    
    @validates('role')
    def validate_role(self, key, role):
        """Validate that role is either 'buyer' or 'farmer'"""
        if role not in ['buyer', 'farmer']:
            raise ValueError("Role must be either 'buyer' or 'farmer'")
        return role
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Animal(db.Model):
    """
    Animal model representing livestock available for sale
    
    Attributes:
        id (int): Unique identifier
        name (str): Animal name/breed
        farmer_id (int): Foreign key to User (farmer)
        available (bool): Availability status
        price (float): Price in Kenyan Shillings
    """
    __tablename__ = 'animal'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    available = db.Column(db.Boolean, default=True, index=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @validates('price')
    def validate_price(self, key, price):
        """Validate that price is positive"""
        if price <= 0:
            raise ValueError("Price must be positive")
        return price
    
    def __repr__(self):
        return f'<Animal {self.name} - KSh {self.price}>'


class Order(db.Model):
    """
    Order model representing purchase orders
    
    Attributes:
        id (int): Unique identifier
        buyer_id (int): Foreign key to User (buyer)
        status (str): Order status (pending, paid, confirmed, rejected)
        created_at (datetime): Order creation timestamp
    """
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    @validates('status')
    def validate_status(self, key, status):
        """Validate order status"""
        valid_statuses = ['pending', 'paid', 'confirmed', 'rejected']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        return status
    
    def to_dict(self):
        """Convert order to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class OrderItem(db.Model):
    """
    OrderItem model representing items within an order
    
    Attributes:
        id (int): Unique identifier
        order_id (int): Foreign key to Order
        animal_id (int): Foreign key to Animal
        farmer_id (int): Foreign key to User (farmer)
        quantity (int): Quantity of animals ordered
    """
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, index=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
        """Validate that quantity is positive"""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return quantity
    
    def to_dict(self):
        """Convert order item to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'animal_id': self.animal_id,
            'farmer_id': self.farmer_id,
            'quantity': self.quantity
        }
    
    def __repr__(self):
        return f'<OrderItem {self.id} - Animal {self.animal_id} x{self.quantity}>'
