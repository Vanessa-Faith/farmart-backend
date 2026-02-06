from datetime import datetime
from app import db

class Animal(db.Model):
    __tablename__ = 'animals'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age_months = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Numeric(10, 2), nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False, default=1)
    images = db.Column(db.JSON, default=list)
    county = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='available')
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    farmer = db.relationship('User', backref='animals')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'breed': self.breed,
            'age_months': self.age_months,
            'price_per_unit': float(self.price_per_unit),
            'quantity_available': self.quantity_available,
            'images': self.images or [],
            'county': self.county,
            'status': self.status,
            'farmer_id': self.farmer_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }