from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order
from app.models.animal import Animal
from app.models.user import User
from app import db

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data.get('animal_id'):
        return jsonify({'error': 'animal_id is required'}), 400
    
    animal = Animal.query.get(data['animal_id'])
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    
    quantity = data.get('quantity', 1)
    if quantity > animal.quantity_available:
        return jsonify({'error': 'Insufficient quantity available'}), 400
    
    total_price = animal.price_per_unit * quantity
    
    order = Order(
        buyer_id=user_id,
        animal_id=animal.id,
        quantity=quantity,
        total_price=total_price,
        status='pending'
    )
    
    # Decrease available quantity
    animal.quantity_available -= quantity
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders for current user (buyer sees their orders, farmer sees orders for their animals)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'farmer':
        # Get orders for animals owned by this farmer
        animals = Animal.query.filter_by(farmer_id=user_id).all()
        animal_ids = [a.id for a in animals]
        orders = Order.query.filter(Order.animal_id.in_(animal_ids)).all()
    else:
        # Buyers see their own orders
        orders = Order.query.filter_by(buyer_id=user_id).all()
    
    return jsonify([order.to_dict() for order in orders]), 200

@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    """Get single order by ID"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check authorization
    if user.role == 'farmer':
        # Farmer can only see orders for their animals
        animal = Animal.query.get(order.animal_id)
        if animal.farmer_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
    else:
        # Buyers can only see their own orders
        if order.buyer_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(order.to_dict()), 200

@orders_bp.route('/<int:id>/confirm', methods=['POST'])
@jwt_required()
def confirm_order(id):
    """Confirm an order (farmer only)"""
    user_id = get_jwt_identity()
    
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    animal = Animal.query.get(order.animal_id)
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized - you can only confirm orders for your own animals'}), 403
    
    if order.status != 'pending':
        return jsonify({'error': 'Order is not in pending status'}), 400
    
    order.status = 'confirmed'
    db.session.commit()
    
    return jsonify(order.to_dict()), 200

@orders_bp.route('/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_order(id):
    """Reject an order (farmer only)"""
    user_id = get_jwt_identity()
    
    order = Order.query.get(id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    animal = Animal.query.get(order.animal_id)
    if animal.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized - you can only reject orders for your own animals'}), 403
    
    if order.status != 'pending':
        return jsonify({'error': 'Order is not in pending status'}), 400
    
    # Restore quantity
    animal.quantity_available += order.quantity
    
    order.status = 'rejected'
    db.session.commit()
    
    return jsonify(order.to_dict()), 200

