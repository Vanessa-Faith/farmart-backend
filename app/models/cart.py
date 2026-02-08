from app import db
from datetime import datetime

class Cart(db.Model):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        """Convert cart to dictionary for API responses"""
        return {
            'id': self.id,
            'buyer_id': self.buyer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'items': [item.to_dict() for item in self.items],
            'total_items': self.items.count(),
            'total_amount': sum(item.quantity * item.animal.price_per_unit for item in self.items)
        }

    def __repr__(self):
        return f'<Cart {self.id} - Buyer {self.buyer_id}>'


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    animal = db.relationship('Animal', backref='cart_items', lazy='select')

    def to_dict(self):
        """Convert cart item to dictionary for API responses"""
        animal = self.animal
        return {
            'id': self.id,
            'cart_id': self.cart_id,
            'animal_id': self.animal_id,
            'quantity': self.quantity,
            'added_at': self.added_at.isoformat() if self.added_at else None,
            'animal': {
                'id': animal.id,
                'title': animal.title,
                'breed': animal.breed,
                'price_per_unit': float(animal.price_per_unit),
                'image': animal.images[0] if animal.images else None,
                'quantity_available': animal.quantity_available
            } if animal else None,
            'subtotal': float(self.quantity * animal.price_per_unit) if animal else 0
        }

    def __repr__(self):
        return f'<CartItem {self.id} - Animal {self.animal_id}>'