from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.cart import Cart, CartItem

carts_bp = Blueprint('carts', __name__)


@carts_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Get current user's cart
    TODO: Handle empty cart case
    """
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(buyer_id=user_id).first()
    
    if not cart:
        # TODO: Create cart if doesn't exist
        return jsonify({'items': [], 'total': 0}), 200
    
    return jsonify(cart.to_dict()), 200


@carts_bp.route('/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add item to cart
    TODO: Validate animal exists and is available
    TODO: Check quantity available
    TODO: Handle existing item (update quantity)
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # TODO: Get or create cart
    # TODO: Add validation
    # TODO: Check if item already in cart
    
    return jsonify({'message': 'Item added to cart'}), 201


@carts_bp.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """
    Update cart item quantity
    TODO: Validate ownership
    TODO: Check available quantity
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # TODO: Implement update logic
    
    return jsonify({'message': 'Cart item updated'}), 200


@carts_bp.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """
    Remove item from cart
    TODO: Validate ownership
    """
    user_id = get_jwt_identity()
    
    # TODO: Implement delete logic
    
    return jsonify({'message': 'Item removed from cart'}), 200
