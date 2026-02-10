from app import create_app, db
from app.models.user import User
from app.models.animal import Animal

def add_sample_data():
    app = create_app()
    
    with app.app_context():
        # Create farmer if doesn't exist
        farmer = User.query.filter_by(email="farmer@example.com").first()
        if not farmer:
            farmer = User(
                email="farmer@example.com",
                first_name="John",
                last_name="Farmer",
                user_type="farmer",
                phone="+254700000000",
                county="Nairobi"
            )
            farmer.set_password("password123")
            db.session.add(farmer)
            db.session.commit()
        
        # Add sample animals
        animals_data = [
            {
                "title": "Premium Holstein Dairy Cow",
                "type": "cow",
                "breed": "Holstein",
                "age_months": 24,
                "price_per_unit": 1500.00,
                "quantity_available": 1,
                "county": "Nairobi",
                "farmer_id": farmer.id
            },
            {
                "title": "Young Angus Bull",
                "type": "cow",
                "breed": "Angus",
                "age_months": 18,
                "price_per_unit": 2000.00,
                "quantity_available": 1,
                "county": "Nakuru",
                "farmer_id": farmer.id
            },
            {
                "title": "Free Range Chickens",
                "type": "chicken",
                "breed": "Rhode Island Red",
                "age_months": 6,
                "price_per_unit": 25.00,
                "quantity_available": 50,
                "county": "Kiambu",
                "farmer_id": farmer.id
            }
        ]
        
        for animal_data in animals_data:
            animal = Animal(**animal_data)
            db.session.add(animal)
        
        db.session.commit()
        print(f"Added {len(animals_data)} sample animals")
        print("Farmer: farmer@example.com / password123")

if __name__ == '__main__':
    add_sample_data()