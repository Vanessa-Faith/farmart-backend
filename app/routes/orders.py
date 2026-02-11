from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
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
@jwt_required()
def get_orders():
    """
    Get orders for the authenticated user.
    
    Returns:
        JSON response with list of orders
        - Buyers see their own orders
        - Farmers see orders containing their animals
    
    Raises:
        404: User not found
        200: Success with orders list
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id, description="User not found")
        
        logger.info(f"User {user.username} ({user.role}) requesting orders")
        
        if user.role == "buyer":
            orders = Order.query.filter_by(buyer_id=user_id).all()
        else:
            orders = (
                Order.query.join(OrderItem)
                .filter(OrderItem.farmer_id == user_id)
                .distinct()
                .all()
            )
        
        logger.info(f"Found {len(orders)} orders for user {user.username}")
        return jsonify([order.to_dict() for order in orders]), 200
        
    except Exception as e:
        logger.error(f"Error retrieving orders for user {user_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve orders"}), 500


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):
    """
    Get a specific order by ID.
    
    Args:
        order_id (int): The ID of the order to retrieve
    
    Returns:
        JSON response with order details
    
    Raises:
        404: Order not found
        403: Unauthorized access
        200: Success with order details
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id, description="User not found")
        order = Order.query.get_or_404(order_id, description="Order not found")
        
        logger.info(f"User {user.username} requesting order {order_id}")
        
        # Authorization checks
        if user.role == "buyer" and order.buyer_id != user_id:
            logger.warning(f"Unauthorized access attempt: buyer {user_id} accessing order {order_id}")
            return jsonify({"error": "Unauthorized"}), 403

        if user.role == "farmer":
            if not any(item.farmer_id == user_id for item in order.items):
                logger.warning(f"Unauthorized access attempt: farmer {user_id} accessing order {order_id}")
                return jsonify({"error": "Unauthorized"}), 403

        logger.info(f"Successfully retrieved order {order_id} for user {user.username}")
        return jsonify(order.to_dict()), 200
        
    except Exception as e:
        logger.error(f"Error retrieving order {order_id}: {str(e)}")
        return jsonify({"error": "Failed to retrieve order"}), 500


@orders_bp.route("", methods=["POST"])
@jwt_required()
def create_order():
    """
    Create a new order.
    
    Only buyers can create orders. Each order can contain multiple animals.
    
    Request Body:
        {
            "items": [
                {
                    "animal_id": 1,
                    "quantity": 2
                }
            ]
        }
    
    Returns:
        JSON response with created order details
    
    Raises:
        403: Only buyers can create orders
        400: Invalid request data
        404: Animal not found or unavailable
        201: Success with created order
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id, description="User not found")

        if user.role != "buyer":
            logger.warning(f"Non-buyer {user_id} attempted to create order")
            return jsonify({"error": "Only buyers can create orders"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        items = data.get("items", [])

        if not items:
            return jsonify({"error": "No items provided"}), 400

        logger.info(f"User {user.username} creating order with {len(items)} items")
        
        # Validate and create order items
        order_items = []
        total_value = 0
        
        for item_data in items:
            animal_id = item_data.get("animal_id")
            quantity = item_data.get("quantity", 1)

            if not animal_id:
                return jsonify({"error": "Animal ID is required for each item"}), 400

            if not isinstance(quantity, int) or quantity <= 0:
                return jsonify({"error": "Quantity must be a positive integer"}), 400

            animal = Animal.query.get(animal_id)
            if not animal:
                return jsonify({"error": f"Animal with ID {animal_id} not found"}), 404
            
            if not animal.available:
                return jsonify({"error": f"Animal with ID {animal_id} is not available"}), 400

            # Calculate item value
            item_value = animal.price * quantity
            total_value += item_value
            
            order_item = OrderItem(
                animal_id=animal.id,
                farmer_id=animal.farmer_id,
                quantity=quantity
            )
            order_items.append(order_item)

        # Create the order
        order = Order(buyer_id=user_id, status="pending")
        db.session.add(order)
        db.session.flush()

        # Add order items
        for order_item in order_items:
            order_item.order_id = order.id
            db.session.add(order_item)

        db.session.commit()
        
        logger.info(f"Order {order.id} created successfully for user {user.username}, total value: KSh {total_value}")
        return jsonify(order.to_dict()), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Database integrity error creating order: {str(e)}")
        return jsonify({"error": "Database constraint violation"}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating order: {str(e)}")
        return jsonify({"error": "Database operation failed"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error creating order: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@orders_bp.route("/<int:order_id>/pay", methods=["POST"])
@jwt_required()
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
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id, description="Order not found")

        # Authorization check
        if order.buyer_id != user_id:
            logger.warning(f"Unauthorized payment attempt: user {user_id} for order {order_id}")
            return jsonify({"error": "Unauthorized"}), 403

        # State validation
        if order.status != "pending":
            logger.warning(f"Invalid payment attempt: order {order_id} is {order.status}, not pending")
            return jsonify({"error": f"Cannot pay for order in '{order.status}' status"}), 400

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
@jwt_required()
def confirm_order(order_id):
    """
    Confirm an order.
    
    Only farmers who have animals in the order can confirm it.
    Order must be in 'paid' status.
    
    Args:
        order_id (int): The ID of the order to confirm
    
    Returns:
        JSON response with success message
    
    Raises:
        404: Order not found
        403: Unauthorized confirmation attempt
        400: Invalid order state for confirmation
        200: Success
    """
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id, description="Order not found")

        # State validation
        if order.status != "paid":
            logger.warning(f"Invalid confirmation attempt: order {order_id} is {order.status}, not paid")
            return jsonify({"error": f"Cannot confirm order in '{order.status}' status"}), 400

        # Authorization check
        if not any(item.farmer_id == user_id for item in order.items):
            logger.warning(f"Unauthorized confirmation attempt: user {user_id} for order {order_id}")
            return jsonify({"error": "Unauthorized"}), 403

        logger.info(f"Confirming order {order_id} by farmer {user_id}")
        
        order.status = "confirmed"
        db.session.commit()
        
        logger.info(f"Order {order_id} confirmed successfully")
        return jsonify({"message": "Order confirmed"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error confirming order {order_id}: {str(e)}")
        return jsonify({"error": "Order confirmation failed"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error confirming order {order_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@orders_bp.route("/<int:order_id>/reject", methods=["POST"])
@jwt_required()
def reject_order(order_id):
    """
    Reject an order.
    
    Only farmers who have animals in the order can reject it.
    
    Args:
        order_id (int): The ID of the order to reject
    
    Returns:
        JSON response with success message
    
    Raises:
        404: Order not found
        403: Unauthorized rejection attempt
        200: Success
    """
    try:
        user_id = get_jwt_identity()
        order = Order.query.get_or_404(order_id, description="Order not found")

        # Authorization check
        if not any(item.farmer_id == user_id for item in order.items):
            logger.warning(f"Unauthorized rejection attempt: user {user_id} for order {order_id}")
            return jsonify({"error": "Unauthorized"}), 403

        logger.info(f"Rejecting order {order_id} by farmer {user_id}")
        
        order.status = "rejected"
        db.session.commit()
        
        logger.info(f"Order {order_id} rejected successfully")
        return jsonify({"message": "Order rejected"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error rejecting order {order_id}: {str(e)}")
        return jsonify({"error": "Order rejection failed"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error rejecting order {order_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
