from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
<<<<<<< HEAD
from app import db
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.animal import Animal
from app.models.user import User

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('', methods=['GET'])
=======
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import func
import logging
import json
from datetime import datetime

from app.models import db, Order, OrderItem, Animal, User
from app.services.mpesa import send_stk_push, MpesaError

logger = logging.getLogger(__name__)
orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


def _normalize_phone_number(phone_number):
    """Normalize Kenyan phone numbers to 2547XXXXXXXX format."""
    if not phone_number:
        return None
    raw = phone_number.strip().replace(" ", "")
    if raw.startswith("+"):
        raw = raw[1:]
    if raw.startswith("0"):
        raw = "254" + raw[1:]
    if not raw.startswith("254") or len(raw) < 12:
        return None
    return raw


def _calculate_order_amount(order_id):
    """Calculate total order amount in KES using current animal prices."""
    total = (
        db.session.query(func.sum(Animal.price * OrderItem.quantity))
        .join(OrderItem, OrderItem.animal_id == Animal.id)
        .filter(OrderItem.order_id == order_id)
        .scalar()
    )
    return float(total or 0)


def _parse_mpesa_callback_items(items):
    parsed = {}
    for item in items or []:
        name = item.get("Name")
        value = item.get("Value")
        if name:
            parsed[name] = value
    return parsed


@orders_bp.route("", methods=["GET"])
>>>>>>> ce230761465cc6fabc28f399185c8b503eaceaaf
@jwt_required()
def get_orders():
    """Get user's orders (buyer sees their purchases, farmer sees orders for their animals)"""
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
    """Get single order details"""
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
    """Create order from cart"""
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


@orders_bp.route('/<int:id>/pay', methods=['POST'])
@jwt_required()
<<<<<<< HEAD
def pay_order(id):
    """Process payment for order"""
    identity = get_jwt_identity()
=======
def pay_order(order_id):
    """
    Initiate M-Pesa STK Push for an order.
    
    Only the buyer who created the order can pay for it.
    Order must be in 'pending' status.
    
    Args:
        order_id (int): The ID of the order to pay for
    
    Request Body:
        {
            "phone_number": "07XXXXXXXX" or "2547XXXXXXXX"
        }

    Returns:
        JSON response with STK Push initiation details
    
    Raises:
        404: Order not found
        403: Unauthorized payment attempt
        400: Invalid order state for payment
        200: STK Push initiated
    """
>>>>>>> ce230761465cc6fabc28f399185c8b503eaceaaf
    try:
        user_id = int(identity)
    except (TypeError, ValueError):
        return jsonify({'message': 'Invalid token identity'}), 422
    
    data = request.get_json(silent=True)

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if user.role != 'buyer':
        return jsonify({'message': 'Only buyers can pay for orders'}), 403

    order = Order.query.get(id)
    if not order:
        return jsonify({'message': 'Order not found'}), 404

<<<<<<< HEAD
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


@orders_bp.route('/<int:id>/confirm', methods=['POST'])
=======
        logger.info(f"Processing payment for order {order_id} by user {user_id}")

        if order.mpesa_checkout_request_id and order.mpesa_result_code is None:
            return jsonify({"error": "Payment already initiated. Please wait for confirmation."}), 409

        data = request.get_json() or {}
        phone_number = _normalize_phone_number(data.get("phone_number"))
        if not phone_number:
            return jsonify({"error": "Valid Kenyan phone_number is required"}), 400

        amount = _calculate_order_amount(order.id)
        if amount <= 0:
            return jsonify({"error": "Order total is invalid"}), 400

        response = send_stk_push(
            amount=round(amount),
            phone_number=phone_number,
            account_reference=f"ORDER-{order.id}",
            transaction_desc=f"Payment for Order {order.id}",
        )

        # Expected success fields for STK Push
        if response.get("ResponseCode") != "0":
            logger.error(f"STK Push failed for order {order.id}: {response}")
            return jsonify({"error": "STK Push failed", "details": response}), 400

        order.mpesa_merchant_request_id = response.get("MerchantRequestID")
        order.mpesa_checkout_request_id = response.get("CheckoutRequestID")
        order.mpesa_request_sent_at = datetime.utcnow()
        order.mpesa_phone_number = phone_number
        order.mpesa_amount = round(amount)
        order.mpesa_result_code = None
        order.mpesa_result_desc = response.get("ResponseDescription")
        db.session.commit()

        logger.info(f"STK Push initiated for order {order_id}")
        return jsonify({
            "message": "STK Push sent. Enter PIN on your phone to complete payment.",
            "checkout_request_id": order.mpesa_checkout_request_id,
            "merchant_request_id": order.mpesa_merchant_request_id,
        }), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error processing payment for order {order_id}: {str(e)}")
        return jsonify({"error": "Payment processing failed"}), 500
    except MpesaError as e:
        db.session.rollback()
        logger.error(f"M-Pesa error processing payment for order {order_id}: {str(e)}")
        return jsonify({"error": "M-Pesa request failed", "details": str(e)}), 502
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error processing payment for order {order_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@orders_bp.route("/mpesa/callback", methods=["POST"])
def mpesa_callback():
    """
    Handle M-Pesa STK Push callback.

    This endpoint is called by Safaricom after the customer approves or rejects the payment.
    """
    try:
        payload = request.get_json(silent=True) or {}
        callback = payload.get("Body", {}).get("stkCallback", {})
        checkout_request_id = callback.get("CheckoutRequestID")

        if not checkout_request_id:
            logger.warning(f"Invalid M-Pesa callback payload: {payload}")
            return jsonify({"ResultCode": 1, "ResultDesc": "Invalid callback"}), 400

        order = Order.query.filter_by(mpesa_checkout_request_id=checkout_request_id).first()
        if not order:
            logger.error(f"No order matches CheckoutRequestID {checkout_request_id}")
            return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

        result_code = callback.get("ResultCode")
        result_desc = callback.get("ResultDesc")
        order.mpesa_result_code = int(result_code) if result_code is not None else None
        order.mpesa_result_desc = result_desc
        order.mpesa_callback_raw = json.dumps(payload)

        if order.mpesa_result_code == 0:
            items = _parse_mpesa_callback_items(
                callback.get("CallbackMetadata", {}).get("Item", [])
            )
            order.mpesa_amount = items.get("Amount", order.mpesa_amount)
            order.mpesa_receipt_number = items.get("MpesaReceiptNumber")
            order.mpesa_phone_number = items.get("PhoneNumber", order.mpesa_phone_number)

            txn_date = items.get("TransactionDate")
            if txn_date:
                try:
                    order.mpesa_transaction_date = datetime.strptime(str(txn_date), "%Y%m%d%H%M%S")
                except ValueError:
                    logger.warning(f"Invalid transaction date in callback: {txn_date}")

            # Only mark as paid after successful confirmation
            order.status = "paid"

        db.session.commit()
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error handling M-Pesa callback: {str(e)}")
        return jsonify({"ResultCode": 1, "ResultDesc": "DB error"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error in M-Pesa callback: {str(e)}")
        return jsonify({"ResultCode": 1, "ResultDesc": "Server error"}), 500


@orders_bp.route("/<int:order_id>/confirm", methods=["POST"])
>>>>>>> ce230761465cc6fabc28f399185c8b503eaceaaf
@jwt_required()
def confirm_order(id):
    """Farmer confirms order"""
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

    return jsonify({'message': 'Order confirmed', 'order': order.to_dict()}), 200


@orders_bp.route('/<int:id>/reject', methods=['POST'])
@jwt_required()
def reject_order(id):
    """Farmer rejects order"""
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

    if order.status in ['rejected', 'confirmed']:
        return jsonify({'message': 'Order cannot be rejected'}), 400

    order.status = 'rejected'

    for item in order.items:
        animal = Animal.query.get(item.animal_id)
        if animal and animal.quantity is not None:
            animal.quantity += item.quantity
            if animal.quantity > 0:
                animal.status = 'available'

    db.session.commit()

    return jsonify({'message': 'Order rejected', 'order': order.to_dict()}), 200


@orders_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_order(id):
    """Update order status (farmer: confirm/reject)"""
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
