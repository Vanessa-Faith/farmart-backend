from app import db
from datetime import datetime


class Animal(db.Model):
    __tablename__ = 'animals'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False, index=True)
    breed = db.Column(db.String(100), index=True)
    age = db.Column(db.Integer)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='available')  # 'available', 'pending', 'sold'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert animal to dictionary"""
        return {
            'id': self.id,
            'farmer_id': self.farmer_id,
            'title': self.title,
            'animal_type': self.animal_type,
            'breed': self.breed,
            'age': self.age,
            'price': float(self.price) if self.price else None,
            'quantity': self.quantity,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Animal {self.title}>'
