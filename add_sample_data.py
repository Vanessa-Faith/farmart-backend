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
                name="John Farmer",  # Use 'name' field as per User model
                email="farmer@example.com",
                role="farmer"  # Use 'role' field, not 'user_type'
            )
            farmer.set_password("password123")
            db.session.add(farmer)
            db.session.commit()
        
        # Add sample animals with correct field names matching Animal model
        animals_data = [
            {
                "title": "Premium Holstein Dairy Cow",
                "animal_type": "Cow",  # 'animal_type' not 'type'
                "breed": "Holstein",
                "age": 24,  # 'age' not 'age_months'
                "price": 1500.00,  # 'price' not 'price_per_unit'
                "quantity": 1,  # 'quantity' not 'quantity_available'
                "description": "High milk production Holstein cow",
                "farmer_id": farmer.id
            },
            {
                "title": "Young Angus Bull",
                "animal_type": "Cow",
                "breed": "Angus",
                "age": 18,
                "price": 2000.00,
                "quantity": 1,
                "description": "Strong breeding bull",
                "farmer_id": farmer.id
            },
            {
                "title": "Free Range Chickens",
                "animal_type": "Chicken",
                "breed": "Rhode Island Red",
                "age": 6,
                "price": 25.00,
                "quantity": 50,
                "description": "Healthy free range chickens",
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
