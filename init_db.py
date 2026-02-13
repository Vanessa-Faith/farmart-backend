"""
Database initialization script for FarmArt Backend
Run this script to create all database tables and add sample data
"""

from app import create_app, db
from app.models.user import User
from app.models.animal import Animal
from app.models.order import Order

def init_database():
    """Initialize database with tables and sample data"""
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created successfully")
        
        # Check if sample data already exists
        if User.query.first():
            print("\n⚠ Database already contains data. Skipping sample data creation.")
            print("To reset database, delete the .db file in instance/ folder")
            return
        
        # Create sample users
        print("\nCreating sample users...")
        
        # Farmer user
        farmer = User(
            username='john_farmer',
            email='farmer@farmart.com',
            role='farmer'
        )
        farmer.set_password('password123')
        
        # Buyer user
        buyer = User(
            username='jane_buyer',
            email='buyer@farmart.com',
            role='buyer'
        )
        buyer.set_password('password123')
        
        db.session.add(farmer)
        db.session.add(buyer)
        db.session.commit()
        
        print(f"✓ Created farmer: {farmer.email} (password: password123)")
        print(f"✓ Created buyer: {buyer.email} (password: password123)")
        
        # Create sample animals
        # Note: type must be one of: cattle, goat, sheep, chicken, pig
        print("\nCreating sample animals...")
        
        animals = [
            Animal(
                title='Holstein Cow',
                type='cattle',
                breed='Holstein',
                age_months=24,
                price_per_unit=3500.00,
                weight_lbs=500,
                quantity_available=1,
                health_status='Healthy',
                county='Nairobi',
                description='Healthy milking cow, produces 30 liters per day',
                farmer_id=farmer.id
            ),
            Animal(
                title='Boer Goat',
                type='goat',
                breed='Boer',
                age_months=12,
                price_per_unit=450.00,
                weight_lbs=80,
                quantity_available=3,
                health_status='Healthy',
                county='Kisumu',
                description='Purebred Boer goat, excellent for breeding',
                farmer_id=farmer.id
            ),
            Animal(
                title='Rhode Island Red Chicken',
                type='chicken',
                breed='Rhode Island Red',
                age_months=6,
                price_per_unit=35.00,
                weight_lbs=3,
                quantity_available=20,
                health_status='Healthy',
                county='Nakuru',
                description='Good egg layers, 250 eggs per year',
                farmer_id=farmer.id
            ),
            Animal(
                title='Merino Sheep',
                type='sheep',
                breed='Merino',
                age_months=18,
                price_per_unit=550.00,
                weight_lbs=60,
                quantity_available=5,
                health_status='Healthy',
                county='Nairobi',
                description='Fine wool sheep, excellent for wool production',
                farmer_id=farmer.id
            ),
            Animal(
                title='Large White Pig',
                type='pig',
                breed='Large White',
                age_months=8,
                price_per_unit=350.00,
                weight_lbs=150,
                quantity_available=4,
                health_status='Healthy',
                county='Eldoret',
                description='Fast growing pig breed, excellent for pork production',
                farmer_id=farmer.id
            ),
        ]
        
        for animal in animals:
            db.session.add(animal)
        
        db.session.commit()
        print(f"✓ Created {len(animals)} sample animals")
        
        print("\n" + "="*50)
        print("Database initialization complete!")
        print("="*50)
        print("\nTest Credentials:")
        print("  Farmer:  farmer@farmart.com / password123")
        print("  Buyer:   buyer@farmart.com / password123")
        print("\nYou can now login at POST /api/auth/login")

if __name__ == '__main__':
    init_database()

