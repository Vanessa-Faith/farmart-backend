from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import Cart, CartItem
from app.models.animal import Animal
from app.models.user import User

carts_bp = Blueprint('carts', __name__)


def _serialize_cart(cart):
    data = cart.to_dict()
    total = 0
    for item in cart.items:
        if item.animal and item.animal.price is not None:
            total += float(item.animal.price) * item.quantity
    data['total'] = total
    return data


@carts_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Get current user's cart
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    cart = Cart.query.filter_by(buyer_id=user_id).first()
    
    if not cart:
        return jsonify({'items': [], 'total': 0}), 200
    
    return jsonify(_serialize_cart(cart)), 200


@carts_bp.route('/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add item to cart
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
    if user.role != 'buyer':
        return jsonify({'message': 'Only buyers can add to cart'}), 403

    if not data:
        return jsonify({'message': 'No data provided'}), 400

    animal_id = data.get('animal_id')
    quantity = data.get('quantity', 1)

    if not animal_id:
        return jsonify({'message': 'animal_id is required'}), 400

    try:
        quantity = int(quantity)
        if quantity < 1:
            return jsonify({'message': 'quantity must be at least 1'}), 400
    except (TypeError, ValueError):
        return jsonify({'message': 'quantity must be an integer'}), 400

    animal = Animal.query.get(animal_id)
    if not animal or animal.status != 'available':
        return jsonify({'message': 'Animal not available'}), 404

    if animal.quantity is not None and quantity > animal.quantity:
        return jsonify({'message': 'Requested quantity exceeds availability'}), 400

    cart = Cart.query.filter_by(buyer_id=user_id).first()
    if not cart:
        cart = Cart(buyer_id=user_id)
        db.session.add(cart)
        db.session.flush()

    existing_item = CartItem.query.filter_by(cart_id=cart.id, animal_id=animal_id).first()
    if existing_item:
        new_qty = existing_item.quantity + quantity
        if animal.quantity is not None and new_qty > animal.quantity:
            return jsonify({'message': 'Requested quantity exceeds availability'}), 400
        existing_item.quantity = new_qty
    else:
        db.session.add(CartItem(cart_id=cart.id, animal_id=animal_id, quantity=quantity))

    db.session.commit()
    return jsonify(_serialize_cart(cart)), 201


@carts_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """
    Update cart item quantity
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    data = request.get_json()

    if not data or 'quantity' not in data:
        return jsonify({'message': 'quantity is required'}), 400

    try:
        quantity = int(data.get('quantity'))
        if quantity < 1:
            return jsonify({'message': 'quantity must be at least 1'}), 400
    except (TypeError, ValueError):
        return jsonify({'message': 'quantity must be an integer'}), 400

    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Cart item not found'}), 404

    if item.cart.buyer_id != user_id:
        return jsonify({'message': 'You do not have access to this cart item'}), 403

    if item.animal and item.animal.quantity is not None and quantity > item.animal.quantity:
        return jsonify({'message': 'Requested quantity exceeds availability'}), 400

    item.quantity = quantity
    db.session.commit()

    return jsonify(item.to_dict()), 200


@carts_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """
    Remove item from cart
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    item = CartItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Cart item not found'}), 404

    if item.cart.buyer_id != user_id:
        return jsonify({'message': 'You do not have access to this cart item'}), 403

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item removed from cart'}), 200
