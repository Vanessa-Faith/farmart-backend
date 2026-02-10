"""
Order management routes for FarmArt Backend Application

This module handles all order-related API endpoints including:
- Order creation and retrieval
- Payment processing
- Order confirmation and rejection
- Authorization and validation
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from app.models import db, Order, OrderItem, Animal, User

# Set up logging
logger = logging.getLogger(__name__)

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


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
    Mark an order as paid.
    
    Only the buyer who created the order can pay for it.
    Order must be in 'pending' status.
    
    Args:
        order_id (int): The ID of the order to pay for
    
    Returns:
        JSON response with success message
    
    Raises:
        404: Order not found
        403: Unauthorized payment attempt
        400: Invalid order state for payment
        200: Success
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
        
        order.status = "paid"
        db.session.commit()
        
        logger.info(f"Order {order_id} marked as paid")
        return jsonify({"message": "Payment successful"}), 200
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error processing payment for order {order_id}: {str(e)}")
        return jsonify({"error": "Payment processing failed"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error processing payment for order {order_id}: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


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
