from app import create_app, db
from app.models.user import User
from app.models.animal import Animal

app = create_app('development')

with app.app_context():
    # Create farmer
    farmer = User.query.filter_by(email='farmer@example.com').first()
    if not farmer:
        farmer = User(name='John Farmer', email='farmer@example.com', role='farmer')
        farmer.set_password('password123')
        db.session.add(farmer)
        db.session.commit()
    
    # Add animals
    animals = [
        {'title': 'Healthy Dairy Cow', 'animal_type': 'Cow', 'breed': 'Holstein', 'age': 3, 'price': 45000, 'quantity': 5, 'description': 'High milk production', 'image_url': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400'},
        {'title': 'Young Bull', 'animal_type': 'Cow', 'breed': 'Angus', 'age': 2, 'price': 35000, 'quantity': 3, 'description': 'Strong and healthy', 'image_url': 'https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400'},
        {'title': 'Laying Hens', 'animal_type': 'Chicken', 'breed': 'Rhode Island Red', 'age': 1, 'price': 500, 'quantity': 20, 'description': 'Excellent egg layers', 'image_url': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400'},
        {'title': 'Boer Goat', 'animal_type': 'Goat', 'breed': 'Boer', 'age': 2, 'price': 8000, 'quantity': 10, 'description': 'Meat goat', 'image_url': 'https://images.unsplash.com/photo-1533318087102-b3ad366ed041?w=400'},
        {'title': 'Dairy Goat', 'animal_type': 'Goat', 'breed': 'Saanen', 'age': 3, 'price': 12000, 'quantity': 5, 'description': 'High milk yield', 'image_url': 'https://images.unsplash.com/photo-1533318087102-b3ad366ed041?w=400'},
        {'title': 'Merino Sheep', 'animal_type': 'Sheep', 'breed': 'Merino', 'age': 2, 'price': 15000, 'quantity': 8, 'description': 'Quality wool', 'image_url': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400'},
        {'title': 'Breeding Pig', 'animal_type': 'Pig', 'breed': 'Large White', 'age': 1, 'price': 18000, 'quantity': 4, 'description': 'Good for breeding', 'image_url': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400'},
        {'title': 'Broiler Chickens', 'animal_type': 'Chicken', 'breed': 'Cobb', 'age': 0, 'price': 300, 'quantity': 50, 'description': 'Ready for market', 'image_url': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400'},
    ]
    
    for animal_data in animals:
        animal = Animal(farmer_id=farmer.id, **animal_data)
        db.session.add(animal)
    
    db.session.commit()
    print(f'Added {len(animals)} animals to database')
