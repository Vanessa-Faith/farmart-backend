from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.animal import Animal
from app.models.user import User
from app.models.order import OrderItem, Order

animals_bp = Blueprint('animals', __name__)


@animals_bp.route('', methods=['GET'])
def get_animals():
    """
    Get all animals with optional filters
    """
    query = Animal.query.filter_by(status='available')

    animal_type = request.args.get('type') or request.args.get('animal_type')
    if animal_type:
        query = query.filter(Animal.animal_type.ilike(f"%{animal_type}%"))

    breed = request.args.get('breed')
    if breed:
        query = query.filter(Animal.breed.ilike(f"%{breed}%"))

    title = request.args.get('title') or request.args.get('search') or request.args.get('q')
    if title:
        query = query.filter(Animal.title.ilike(f"%{title}%"))

    min_age = request.args.get('min_age')
    max_age = request.args.get('max_age')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')

    try:
        if min_age is not None:
            query = query.filter(Animal.age >= int(min_age))
        if max_age is not None:
            query = query.filter(Animal.age <= int(max_age))
        if min_price is not None:
            query = query.filter(Animal.price >= float(min_price))
        if max_price is not None:
            query = query.filter(Animal.price <= float(max_price))
    except ValueError:
        return jsonify({'message': 'Invalid filter value'}), 400

    page = request.args.get('page')
    per_page = request.args.get('per_page')
    if page or per_page:
        try:
            page = int(page or 1)
            per_page = int(per_page or 20)
            if page < 1 or per_page < 1:
                raise ValueError
        except ValueError:
            return jsonify({'message': 'Invalid pagination values'}), 400
        query = query.offset((page - 1) * per_page).limit(per_page)

    animals = query.all()
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
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    data = request.get_json()

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can create listings'}), 403

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    required_fields = ['title', 'animal_type', 'price']
    for field in required_fields:
        if data.get(field) in [None, '']:
            return jsonify({'message': f'{field} is required'}), 400

    try:
        price = float(data.get('price'))
    except (TypeError, ValueError):
        return jsonify({'message': 'price must be a number'}), 400

    try:
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            return jsonify({'message': 'quantity must be at least 1'}), 400
    except (TypeError, ValueError):
        return jsonify({'message': 'quantity must be an integer'}), 400

    age = data.get('age')
    if age is not None:
        try:
            age = int(age)
        except (TypeError, ValueError):
            return jsonify({'message': 'age must be an integer'}), 400
    
    animal = Animal(
        farmer_id=user_id,
        title=data.get('title'),
        animal_type=data.get('animal_type'),
        breed=data.get('breed'),
        age=age,
        price=price,
        quantity=quantity,
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
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    animal = Animal.query.get(id)
    
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can update listings'}), 403
    if animal.farmer_id != user_id:
        return jsonify({'message': 'You do not own this animal'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400

    if 'title' in data:
        animal.title = data.get('title')
    if 'animal_type' in data:
        animal.animal_type = data.get('animal_type')
    if 'breed' in data:
        animal.breed = data.get('breed')
    if 'description' in data:
        animal.description = data.get('description')
    if 'age' in data:
        try:
            animal.age = int(data.get('age')) if data.get('age') is not None else None
        except (TypeError, ValueError):
            return jsonify({'message': 'age must be an integer'}), 400
    if 'price' in data:
        try:
            animal.price = float(data.get('price'))
        except (TypeError, ValueError):
            return jsonify({'message': 'price must be a number'}), 400
    if 'quantity' in data:
        try:
            quantity = int(data.get('quantity'))
            if quantity < 0:
                return jsonify({'message': 'quantity must be 0 or more'}), 400
            animal.quantity = quantity
        except (TypeError, ValueError):
            return jsonify({'message': 'quantity must be an integer'}), 400
    if 'status' in data:
        animal.status = data.get('status')
    
    db.session.commit()
    return jsonify(animal.to_dict()), 200


@animals_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_animal(id):
    """
    Delete animal listing (owner only)
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    animal = Animal.query.get(id)
    
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can delete listings'}), 403
    if animal.farmer_id != user_id:
        return jsonify({'message': 'You do not own this animal'}), 403

    any_order_exists = (
        db.session.query(OrderItem)
        .filter(OrderItem.animal_id == animal.id)
        .first()
        is not None
    )
    if any_order_exists:
        return jsonify({'message': 'Cannot delete animal that is in an order'}), 409
    
    # TODO: Verify ownership
    
    db.session.delete(animal)
    db.session.commit()
    
    return jsonify({'message': 'Animal deleted successfully'}), 200
