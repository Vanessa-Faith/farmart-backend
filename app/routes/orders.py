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
    try:
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
        animal.quantity_available -= quantity
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201

    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders for current user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role == 'farmer':
            animals = Animal.query.filter_by(farmer_id=user_id).all()
            animal_ids = [a.id for a in animals]
            orders = Order.query.filter(Order.animal_id.in_(animal_ids)).all()
        else:
            orders = Order.query.filter_by(buyer_id=user_id).all()

        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'error': f'Internal Server Error: {str(e)}'}), 500



