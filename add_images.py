from app import create_app, db
from app.models.animal import Animal

app = create_app('development')

# Placeholder images from a free service
placeholders = {
    'Cow': 'https://images.unsplash.com/photo-1516467508483-a7212febe31a?w=400',
    'Chicken': 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400',
    'Goat': 'https://images.unsplash.com/photo-1533318087102-b3ad366ed041?w=400',
    'Sheep': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400',
    'Pig': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400'
}

with app.app_context():
    animals = Animal.query.all()
    for animal in animals:
        if not animal.image_url:
            animal.image_url = placeholders.get(animal.animal_type, 'https://via.placeholder.com/400x300?text=Animal')
    db.session.commit()
    print(f'Updated {len(animals)} animals with placeholder images')
