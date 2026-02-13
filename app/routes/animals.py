from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.animal import Animal
from app.models.user import User
from app import db

animals_bp = Blueprint('animals', __name__)

@animals_bp.route('', methods=['GET'])
def get_animals():
    """Get all animals"""
    animals = Animal.query.all()
    return jsonify([animal.to_dict() for animal in animals]), 200

@animals_bp.route('/<int:id>', methods=['GET'])
def get_animal(id):
    """Get single animal by ID"""
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    return jsonify(animal.to_dict()), 200

@animals_bp.route('', methods=['POST'])
@jwt_required()
def create_animal():
    """Create a new animal (farmers only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'farmer':
        return jsonify({'error': 'Only farmers can create animals'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'breed', 'type', 'age_months', 'price_per_unit']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate animal type
    valid_types = ['cattle', 'goat', 'sheep', 'chicken', 'pig']
    if data['type'] not in valid_types:
        return jsonify({'error': f'Invalid animal type. Must be one of: {", ".join(valid_types)}'}), 400
    
    animal = Animal(
        title=data['title'],
        breed=data['breed'],
        type=data['type'],
        age_months=data['age_months'],
        price_per_unit=data['price_per_unit'],
        weight_lbs=data.get('weight_lbs'),
        quantity_available=data.get('quantity_available', 1),
        health_status=data.get('health_status'),
        county=data.get('county'),
        description=data.get('description'),
        images=data.get('images', []),
        farmer_id=user_id
    )
    
    db.session.add(animal)
    db.session.commit()
    
    return jsonify(animal.to_dict()), 201

@animals_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_animal(id):
    """Update an animal (owner only)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized - you can only update your own animals'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        animal.title = data['title']
    if 'breed' in data:
        animal.breed = data['breed']
    if 'type' in data:
        valid_types = ['cattle', 'goat', 'sheep', 'chicken', 'pig']
        if data['type'] not in valid_types:
            return jsonify({'error': f'Invalid animal type'}), 400
        animal.type = data['type']
    if 'age_months' in data:
        animal.age_months = data['age_months']
    if 'price_per_unit' in data:
        animal.price_per_unit = data['price_per_unit']
    if 'weight_lbs' in data:
        animal.weight_lbs = data['weight_lbs']
    if 'quantity_available' in data:
        animal.quantity_available = data['quantity_available']
    if 'health_status' in data:
        animal.health_status = data['health_status']
    if 'county' in data:
        animal.county = data['county']
    if 'description' in data:
        animal.description = data['description']
    if 'images' in data:
        animal.images = data['images']
    
    db.session.commit()
    
    return jsonify(animal.to_dict()), 200

@animals_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_animal(id):
    """Delete an animal (owner only)"""
    user_id = get_jwt_identity()
    
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized - you can only delete your own animals'}), 403
    
    db.session.delete(animal)
    db.session.commit()
    
    return jsonify({'message': 'Animal deleted successfully'}), 200

