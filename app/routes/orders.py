from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.animal import Animal
from app.models.user import User

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """
    Get user's orders (buyer sees their purchases, farmer sees orders for their animals)
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 'farmer':
        orders = (
            Order.query
            .join(OrderItem, OrderItem.order_id == Order.id)
            .filter(OrderItem.farmer_id == user_id)
            .distinct()
            .all()
        )
    else:
        orders = Order.query.filter_by(buyer_id=user_id).all()
    
    return jsonify([order.to_dict() for order in orders]), 200


@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
    """
    Get single order details
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    order = Order.query.get(id)
    
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user.role == 'farmer':
        has_access = any(item.farmer_id == user_id for item in order.items)
        if not has_access:
            return jsonify({'message': 'Access denied'}), 403
    else:
        if order.buyer_id != user_id:
            return jsonify({'message': 'Access denied'}), 403

    return jsonify(order.to_dict()), 200


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """
    Create order from cart
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'buyer':
        return jsonify({'message': 'Only buyers can place orders'}), 403

    cart = Cart.query.filter_by(buyer_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty'}), 400

    total_amount = 0
    order_items = []

    for item in cart.items:
        animal = Animal.query.get(item.animal_id)
        if not animal or animal.status != 'available':
            return jsonify({'message': f'Animal {item.animal_id} not available'}), 400
        if animal.quantity is not None and item.quantity > animal.quantity:
            return jsonify({'message': f'Insufficient quantity for animal {item.animal_id}'}), 400

        unit_price = float(animal.price)
        total_amount += unit_price * item.quantity

        order_items.append({
            'animal_id': animal.id,
            'farmer_id': animal.farmer_id,
            'quantity': item.quantity,
            'unit_price': unit_price
        })

    order = Order(buyer_id=user_id, total_amount=total_amount, status='pending')
    db.session.add(order)
    db.session.flush()

    for item in order_items:
        db.session.add(OrderItem(
            order_id=order.id,
            animal_id=item['animal_id'],
            farmer_id=item['farmer_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price']
        ))

        animal = Animal.query.get(item['animal_id'])
        if animal and animal.quantity is not None:
            animal.quantity -= item['quantity']
            if animal.quantity <= 0:
                animal.quantity = 0
                animal.status = 'sold'

    for cart_item in list(cart.items):
        db.session.delete(cart_item)

    db.session.commit()
    return jsonify(order.to_dict()), 201


@orders_bp.route('/<int:id>/confirm', methods=['POST'])
@jwt_required()
def confirm_order(id):
    """
    Farmer confirms order
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can confirm orders'}), 403

    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    if not order.items or any(item.farmer_id != user_id for item in order.items):
        return jsonify({'message': 'Access denied'}), 403

    if order.status in ['rejected', 'paid']:
        return jsonify({'message': 'Order cannot be confirmed'}), 400

    order.status = 'confirmed'
    db.session.commit()

    return jsonify({'message': 'Order confirmed'}), 200


@orders_bp.route('/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_order(id):
    """
    Farmer rejects order
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can reject orders'}), 403

    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    if not order.items or any(item.farmer_id != user_id for item in order.items):
        return jsonify({'message': 'Access denied'}), 403

    if order.status in ['rejected', 'paid']:
        return jsonify({'message': 'Order cannot be rejected'}), 400

    order.status = 'rejected'

    for item in order.items:
        animal = Animal.query.get(item.animal_id)
        if animal and animal.quantity is not None:
            animal.quantity += item.quantity
            if animal.quantity > 0:
                animal.status = 'available'

    db.session.commit()

    return jsonify({'message': 'Order rejected'}), 200


@orders_bp.route('/<int:id>/pay', methods=['POST'])
@jwt_required()
def pay_order(id):
    """
    Process payment for order
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
        return jsonify({'message': 'Only buyers can pay for orders'}), 403

    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    if order.buyer_id != user_id:
        return jsonify({'message': 'Access denied'}), 403

    if order.status == 'paid':
        return jsonify({'message': 'Order already paid'}), 400

    if order.status == 'rejected':
        return jsonify({'message': 'Cannot pay a rejected order'}), 400

    provider = 'mock'
    provider_transaction_id = None
    if data:
        provider = data.get('provider', provider)
        provider_transaction_id = data.get('provider_transaction_id')

    payment = Payment(
        order_id=order.id,
        amount=order.total_amount,
        provider=provider,
        provider_transaction_id=provider_transaction_id,
        status='succeeded'
    )
    db.session.add(payment)

    order.status = 'paid'
    db.session.commit()

    return jsonify({'message': 'Payment processed', 'payment': payment.to_dict(), 'order': order.to_dict()}), 200
