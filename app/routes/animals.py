from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.animal import Animal

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('', methods=['GET'])
def get_animals():
    """
    Get all animals with optional filters
    TODO: Implement search by type, breed
    TODO: Implement filtering by age, price range
    TODO: Add pagination
    """
    # TODO: Get query parameters for filters
    animals = Animal.query.filter_by(status='available').all()
    return jsonify([animal.to_dict() for animal in animals]), 200


@animals_bp.route('/<int:id>', methods=['GET'])
def get_animal(id):
    """
    Get single animal by ID
    TODO: Add error handling for not found
    """
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404
    
    return jsonify(animal.to_dict()), 200


@animals_bp.route('', methods=['POST'])
@jwt_required()
def create_animal():
    """
    Create a new animal listing (farmers only)
    TODO: Verify user is a farmer
    TODO: Add validation
    TODO: Handle image uploads
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # TODO: Validate required fields
    animal = Animal(
        farmer_id=user_id,
        title=data.get('title'),
        animal_type=data.get('animal_type'),
        breed=data.get('breed'),
        age=data.get('age'),
        price=data.get('price'),
        quantity=data.get('quantity', 1),
        description=data.get('description')
    )
    
    db.session.add(animal)
    db.session.commit()
    
    return jsonify(animal.to_dict()), 201


@animals_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_animal(id):
    """
    Update animal listing (owner only)
    TODO: Verify ownership
    TODO: Add validation
    """
    user_id = get_jwt_identity()
    animal = Animal.query.get(id)
    
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404
    
    # TODO: Check if user is the farmer who owns this animal
    
    data = request.get_json()
    # TODO: Update fields
    # TODO: Update updated_at timestamp
    
    db.session.commit()
    return jsonify(animal.to_dict()), 200


@animals_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_animal(id):
    """
    Delete animal listing (owner only)
    TODO: Verify ownership
    TODO: Check if animal is in any pending orders
    """
    user_id = get_jwt_identity()
    animal = Animal.query.get(id)
    
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404
    
    # TODO: Verify ownership
    
    db.session.delete(animal)
    db.session.commit()
    
    return jsonify({'message': 'Animal deleted successfully'}), 200
