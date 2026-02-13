import os

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.animal import Animal
from app.models.user import User
from app.services.mpesa import send_stk_push, MpesaError

orders_bp = Blueprint('orders', __name__)


def _serialize_order_for_user(order, user):
    """Serialize order and expose allowed UI actions for current user."""
    data = order.to_dict()
    is_order_farmer = user.role == 'farmer' and any(item.farmer_id == user.id for item in order.items)
    is_order_buyer = user.role == 'buyer' and order.buyer_id == user.id

    data['actions'] = {
        'can_pay': is_order_buyer and order.status == 'pending',
        'can_confirm': is_order_farmer and order.status not in ['rejected', 'confirmed'],
        'can_reject': is_order_farmer and order.status == 'pending',
    }
    return data


@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
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

    return jsonify([_serialize_order_for_user(order, user) for order in orders]), 200


@orders_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_order(id):
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

    return jsonify(_serialize_order_for_user(order, user)), 200


@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
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
            'unit_price': unit_price,
            'animal_image_url': animal.image_url
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
            unit_price=item['unit_price'],
            animal_image_url=item['animal_image_url']
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


@orders_bp.route('/<int:id>/pay', methods=['POST'])
@jwt_required()
def pay_order(id):
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity', 'error_code': 'PAYMENT_INVALID_TOKEN'}), 422
    
    data = request.get_json(silent=True)
    if data is not None and not isinstance(data, dict):
        return jsonify({'message': 'Invalid JSON payload', 'error_code': 'PAYMENT_INVALID_PAYLOAD'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found', 'error_code': 'PAYMENT_USER_NOT_FOUND'}), 404
    if user.role != 'buyer':
        return jsonify({'message': 'Only buyers can pay for orders', 'error_code': 'PAYMENT_ROLE_FORBIDDEN'}), 403

    # Always resolve the order using the URL param id.
    order_id = id
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'message': 'Order not found', 'error_code': 'PAYMENT_ORDER_NOT_FOUND'}), 404

    if order.buyer_id != user_id:
        return jsonify({'message': 'Access denied', 'error_code': 'PAYMENT_ACCESS_DENIED'}), 403

    existing_payment = (
        Payment.query
        .filter_by(order_id=order.id, status='succeeded')
        .order_by(Payment.created_at.desc(), Payment.id.desc())
        .first()
    )

    if existing_payment:
        if order.status != 'paid':
            order.status = 'paid'
            db.session.commit()
        current_app.logger.info(
            "Payment idempotent success: order_id=%s user_id=%s payment_id=%s",
            order.id,
            user_id,
            existing_payment.id
        )
        return jsonify({
            'message': 'Order already paid',
            'error_code': 'PAYMENT_ALREADY_PAID',
            'payment': existing_payment.to_dict(),
            'order': _serialize_order_for_user(order, user)
        }), 200

    if order.status == 'paid':
        current_app.logger.info(
            "Payment paid-status with missing record: order_id=%s user_id=%s",
            order.id,
            user_id
        )
        return jsonify({
            'message': 'Order already paid',
            'error_code': 'PAYMENT_ALREADY_PAID',
            'payment': None,
            'order': _serialize_order_for_user(order, user)
        }), 200

    if order.status == 'rejected':
        return jsonify({'message': 'Cannot pay a rejected order', 'error_code': 'PAYMENT_REJECTED_ORDER'}), 400

    provider = 'mock'
    provider_transaction_id = None
    if data:
        provider = data.get('provider', provider)
        provider_transaction_id = data.get('provider_transaction_id')

    current_app.logger.info(
        "Payment attempt: order_id=%s user_id=%s provider=%s",
        order.id,
        user_id,
        provider
    )

    if provider == 'mpesa':
        phone_number = None
        if data:
            phone_number = data.get('phone_number')
        phone_number = phone_number or os.getenv('MPESA_TEST_PHONE') or current_app.config.get('MPESA_TEST_PHONE')
        if not phone_number:
            return jsonify({
                'message': 'phone_number is required for M-Pesa payments',
                'error_code': 'PAYMENT_PHONE_REQUIRED'
            }), 400

        try:
            stk_response = send_stk_push(
                amount=order.total_amount,
                phone_number=phone_number,
                account_reference=f"ORDER-{order.id}",
                transaction_desc=f"Payment for order {order.id}",
            )
        except MpesaError as exc:
            current_app.logger.exception(
                "M-Pesa request failed: order_id=%s user_id=%s error=%s",
                order.id,
                user_id,
                str(exc)
            )
            return jsonify({
                'message': 'M-Pesa request failed',
                'error_code': 'PAYMENT_MPESA_ERROR',
                'details': str(exc)
            }), 502

        provider_transaction_id = stk_response.get('CheckoutRequestID') or provider_transaction_id
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            provider=provider,
            provider_transaction_id=provider_transaction_id,
            status='pending'
        )
        db.session.add(payment)
    else:
        payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            provider=provider,
            provider_transaction_id=provider_transaction_id,
            status='succeeded'
        )
        db.session.add(payment)
        order.status = 'paid'

    try:
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        current_app.logger.exception(
            "Payment DB failure: order_id=%s user_id=%s provider=%s error=%s",
            order.id,
            user_id,
            provider,
            str(exc)
        )
        return jsonify({
            'message': 'Payment processing failed',
            'error_code': 'PAYMENT_DB_ERROR'
        }), 500

    current_app.logger.info(
        "Payment success: order_id=%s user_id=%s payment_id=%s status=%s",
        order.id,
        user_id,
        payment.id,
        payment.status
    )

    response = {
        'message': 'Payment initiated' if provider == 'mpesa' else 'Payment processed',
        'payment': payment.to_dict(),
        'order': _serialize_order_for_user(order, user)
    }
    if provider == 'mpesa':
        response['checkout_request_id'] = provider_transaction_id
        response['provider_response'] = stk_response

    return jsonify(response), 200


@orders_bp.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    """Handle Safaricom M-Pesa callback."""
    payload = request.get_json(silent=True) or {}
    callback = ((payload.get('Body') or {}).get('stkCallback') or {})

    checkout_request_id = callback.get('CheckoutRequestID')
    result_code = callback.get('ResultCode')

    if checkout_request_id is None:
        current_app.logger.warning("M-Pesa callback missing CheckoutRequestID: %s", payload)
        return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200

    payment = (
        Payment.query
        .filter_by(provider='mpesa', provider_transaction_id=checkout_request_id)
        .order_by(Payment.created_at.desc(), Payment.id.desc())
        .first()
    )
    if not payment:
        current_app.logger.warning(
            "M-Pesa callback payment not found: checkout_request_id=%s payload=%s",
            checkout_request_id,
            payload
        )
        return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200

    order = Order.query.get(payment.order_id)
    if not order:
        current_app.logger.warning(
            "M-Pesa callback order not found: checkout_request_id=%s payment_id=%s",
            checkout_request_id,
            payment.id
        )
        return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200

    try:
        if result_code == 0:
            payment.status = 'succeeded'
            order.status = 'paid'
        else:
            payment.status = 'failed'
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        current_app.logger.exception(
            "M-Pesa callback DB failure: checkout_request_id=%s order_id=%s error=%s",
            checkout_request_id,
            order.id,
            str(exc)
        )
        return jsonify({'message': 'Callback processing failed'}), 500

    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200


@orders_bp.route('/<int:id>/confirm', methods=['POST'])
@jwt_required()
def confirm_order(id):
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

    if not order.items or not any(item.farmer_id == user_id for item in order.items):
        return jsonify({'message': 'Access denied'}), 403

    if order.status in ['rejected', 'confirmed']:
        return jsonify({'message': 'Order cannot be confirmed'}), 400

    order.status = 'confirmed'
    db.session.commit()

    return jsonify({'message': 'Order confirmed', 'order': _serialize_order_for_user(order, user)}), 200


@orders_bp.route('/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_order(id):
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

    if not order.items or not any(item.farmer_id == user_id for item in order.items):
        return jsonify({'message': 'Access denied'}), 403

    if order.status != 'pending':
        return jsonify({'message': f"Cannot reject order in '{order.status}' status"}), 400

    order.status = 'rejected'

    for item in order.items:
        animal = Animal.query.get(item.animal_id)
        if animal and animal.quantity is not None:
            animal.quantity += item.quantity
            if animal.quantity > 0:
                animal.status = 'available'

    db.session.commit()

    return jsonify({'message': 'Order rejected', 'order': _serialize_order_for_user(order, user)}), 200


@orders_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    """
    Update the status of an order as a farmer (confirm or reject).
    Only the farmer associated with the order can update it.
    Order must not be already finalized.

    Args:
        id (int): Order ID

    Returns:
        Response: JSON order details, 200 status code, or error message.
    """
    identity = get_jwt_identity()
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422

    data = request.get_json(silent=True)
    if not data or 'status' not in data:
        return jsonify({'message': 'Status is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'farmer':
        return jsonify({'message': 'Only farmers can update order status'}), 403

    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    if not order.items or not any(item.farmer_id == user_id for item in order.items):
        return jsonify({'message': 'Access denied'}), 403

    new_status = data.get('status')
    if new_status not in ['confirmed', 'rejected']:
        return jsonify({'message': 'Invalid status. Must be confirmed or rejected'}), 400

    if order.status in ['rejected', 'confirmed']:
        return jsonify({'message': 'Order already finalized'}), 400

    order.status = new_status

    if new_status == 'rejected':
        for item in order.items:
            animal = Animal.query.get(item.animal_id)
            if animal and animal.quantity is not None:
                animal.quantity += item.quantity
                if animal.quantity > 0:
                    animal.status = 'available'

    db.session.commit()

    return jsonify({'message': f'Order {new_status}', 'order': order.to_dict()}), 200
