from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order, OrderItem
from app.models.payment import Payment

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """
    Get user's orders (buyer sees their purchases, farmer sees orders for their animals)
    TODO: Implement role-based filtering
    TODO: Add pagination
    """
    user_id = get_jwt_identity()
    
    # TODO: Filter based on user role
    orders = Order.query.filter_by(buyer_id=user_id).all()
    
    return jsonify([order.to_dict() for order in orders]), 200


@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    """
    Get single order details
    TODO: Verify access (buyer or farmer of items in order)
    """
    user_id = get_jwt_identity()
    order = Order.query.get(id)
    
    if not order:
        return jsonify({'message': 'Order not found'}), 404
    
    # TODO: Verify user has access to this order
    
    return jsonify(order.to_dict()), 200


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """
    Create order from cart
    TODO: Validate cart has items
    TODO: Check animal availability
    TODO: Calculate total
    TODO: Create order items
    TODO: Clear cart after order creation
    """
    user_id = get_jwt_identity()
    
    # TODO: Get user's cart
    # TODO: Validate cart is not empty
    # TODO: Create order and order items
    # TODO: Update animal quantities
    
    return jsonify({'message': 'Order created successfully'}), 201


@orders_bp.route('/<int:id>/confirm', methods=['POST'])
@jwt_required()
def confirm_order(id):
    """
    Farmer confirms order
    TODO: Verify user is the farmer
    TODO: Update order status
    TODO: Send notification to buyer
    """
    user_id = get_jwt_identity()
    
    # TODO: Get order
    # TODO: Verify farmer owns items in order
    # TODO: Update status to 'confirmed'
    
    return jsonify({'message': 'Order confirmed'}), 200


@orders_bp.route('/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_order(id):
    """
    Farmer rejects order
    TODO: Verify user is the farmer
    TODO: Update order status
    TODO: Restore animal quantities
    TODO: Send notification to buyer
    """
    user_id = get_jwt_identity()
    
    # TODO: Get order
    # TODO: Verify farmer owns items in order
    # TODO: Update status to 'rejected'
    # TODO: Restore inventory
    
    return jsonify({'message': 'Order rejected'}), 200


@orders_bp.route('/<int:id>/pay', methods=['POST'])
@jwt_required()
def pay_order(id):
    """
    Process payment for order
    TODO: Integrate payment provider (Stripe/mock)
    TODO: Create payment record
    TODO: Update order status
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # TODO: Verify order belongs to user
    # TODO: Process payment
    # TODO: Create payment record
    # TODO: Update order status to 'paid'
    
    return jsonify({'message': 'Payment processed'}), 200
