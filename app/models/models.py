from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    role = db.Column(db.String(20), nullable=False, index=True)
    
    # Relationships
    animals = db.relationship('Animal', backref='farmer', lazy=True)
    orders = db.relationship('Order', backref='buyer', lazy=True)
    
    @validates('role')
    def validate_role(self, key, role):
        if role not in ['buyer', 'farmer']:
            raise ValueError("Role must be either 'buyer' or 'farmer'")
        return role
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Animal(db.Model):
    __tablename__ = 'animal'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    available = db.Column(db.Boolean, default=True, index=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @validates('price')
    def validate_price(self, key, price):
        if price <= 0:
            raise ValueError("Price must be positive")
        return price
    
    def __repr__(self):
        return f'<Animal {self.name} - KSh {self.price}>'


class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # M-Pesa payment fields
    mpesa_merchant_request_id = db.Column(db.String(100), index=True)
    mpesa_checkout_request_id = db.Column(db.String(100), index=True, unique=False)
    mpesa_result_code = db.Column(db.Integer, index=True)
    mpesa_result_desc = db.Column(db.String(255))
    mpesa_receipt_number = db.Column(db.String(50), index=True)
    mpesa_transaction_date = db.Column(db.DateTime)
    mpesa_phone_number = db.Column(db.String(20))
    mpesa_amount = db.Column(db.Float)
    mpesa_callback_raw = db.Column(db.Text)
    mpesa_request_sent_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    @validates('status')
    def validate_status(self, key, status):
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
            'items': [item.to_dict() for item in self.items],
            'payment': {
                'mpesa_checkout_request_id': self.mpesa_checkout_request_id,
                'mpesa_receipt_number': self.mpesa_receipt_number,
                'mpesa_result_code': self.mpesa_result_code,
                'mpesa_result_desc': self.mpesa_result_desc,
                'mpesa_amount': self.mpesa_amount,
                'mpesa_phone_number': self.mpesa_phone_number,
                'mpesa_transaction_date': (
                    self.mpesa_transaction_date.isoformat() if self.mpesa_transaction_date else None
                ),
            }
        }
    
    def __repr__(self):
        return f'<Order {self.id} - {self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, index=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False, index=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    
    @validates('quantity')
    def validate_quantity(self, key, quantity):
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
