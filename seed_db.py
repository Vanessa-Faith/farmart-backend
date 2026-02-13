#!/usr/bin/env python3
"""Seed production database with sample data"""
from app import create_app, db
from app.models.user import User
from app.models.animal import Animal

def seed_database():
    app = create_app()
    
    with app.app_context():
        print("Seeding database...")
        
        # Create farmer
        farmer = User.query.filter_by(email="farmer@farmart.com").first()
        if not farmer:
            farmer = User(name="John Farmer", email="farmer@farmart.com", role="farmer")
            farmer.set_password("Farmer123!")
            db.session.add(farmer)
            db.session.commit()
            print("✓ Farmer created: farmer@farmart.com / Farmer123!")
        
        # Create buyer
        buyer = User.query.filter_by(email="buyer@farmart.com").first()
        if not buyer:
            buyer = User(name="Jane Buyer", email="buyer@farmart.com", role="buyer")
            buyer.set_password("Buyer123!")
            db.session.add(buyer)
            db.session.commit()
            print("✓ Buyer created: buyer@farmart.com / Buyer123!")
        
        # Add animals
        if Animal.query.count() == 0:
            animals = [
                Animal(title="Holstein Dairy Cow", animal_type="Cow", breed="Holstein", age=24, price=1500, quantity=3, description="High milk production", farmer_id=farmer.id),
                Animal(title="Angus Bull", animal_type="Cow", breed="Angus", age=18, price=2000, quantity=2, description="Strong breeding bull", farmer_id=farmer.id),
                Animal(title="Free Range Chickens", animal_type="Chicken", breed="Rhode Island Red", age=6, price=25, quantity=50, description="Healthy chickens", farmer_id=farmer.id),
            ]
            db.session.add_all(animals)
            db.session.commit()
            print(f"✓ Added {len(animals)} animals")
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
