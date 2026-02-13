from app import db
from datetime import datetime

class Animal(db.Model):
    __tablename__ = 'animals'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # cattle, goat, sheep, chicken, pig
    age_months = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    weight_lbs = db.Column(db.Float)
    quantity_available = db.Column(db.Integer, default=1)
    health_status = db.Column(db.String(200))
    county = db.Column(db.String(50))
    description = db.Column(db.Text)
    images = db.Column(db.JSON)  # Store array of image URLs
    farmer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'breed': self.breed,
            'type': self.type,
            'age_months': self.age_months,
            'price_per_unit': self.price_per_unit,
            'weight_lbs': self.weight_lbs,
            'quantity_available': self.quantity_available,
            'health_status': self.health_status,
            'county': self.county,
            'description': self.description,
            'images': self.images or [],
            'farmer_id': self.farmer_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

