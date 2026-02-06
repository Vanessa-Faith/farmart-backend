from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order
from app.models.order_item import OrderItem
from app import db

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")


@orders_bp.route("", methods=["GET"])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    role = get_jwt_identity().get("role") if isinstance(get_jwt_identity(), dict) else None

    if role == "farmer":
        orders = Order.query.join(OrderItem).filter(OrderItem.farmer_id == user_id).distinct().all()
    else:
        orders = Order.query.filter_by(buyer_id=user_id).all()

    return jsonify([
        {
            "id": o.id,
            "status": o.status,
            "created_at": o.created_at.isoformat(),
            "items": [
                {
                    "id": i.id,
                    "animal_id": i.animal_id,
                    "farmer_id": i.farmer_id,
                    "price": i.price
                } for i in o.items
            ]
        } for o in orders
    ])


@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order_detail(order_id):
    user_id = get_jwt_identity()
    role = get_jwt_identity().get("role") if isinstance(get_jwt_identity(), dict) else None
    
    order = Order.query.get_or_404(order_id)
    
    if role == "farmer":
        if not any(i.farmer_id == user_id for i in order.items):
            return jsonify({"error": "Unauthorized"}), 403
    elif order.buyer_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    return jsonify({
        "id": order.id,
        "buyer_id": order.buyer_id,
        "status": order.status,
        "created_at": order.created_at.isoformat(),
        "items": [
            {
                "id": i.id,
                "animal_id": i.animal_id,
                "farmer_id": i.farmer_id,
                "price": i.price
            } for i in order.items
        ]
    })


@orders_bp.route("/<int:order_id>/confirm", methods=["POST"])
@jwt_required()
def confirm_order(order_id):
    user_id = get_jwt_identity()
    role = get_jwt_identity().get("role") if isinstance(get_jwt_identity(), dict) else None
    
    if role != "farmer":
        return jsonify({"error": "Only farmers can confirm orders"}), 403
    
    order = Order.query.get_or_404(order_id)
    
    if not any(i.farmer_id == user_id for i in order.items):
        return jsonify({"error": "Unauthorized"}), 403
    
    order.status = "confirmed"
    db.session.commit()
    return jsonify({"message": "Order confirmed"})


@orders_bp.route("/<int:order_id>/reject", methods=["POST"])
@jwt_required()
def reject_order(order_id):
    user_id = get_jwt_identity()
    role = get_jwt_identity().get("role") if isinstance(get_jwt_identity(), dict) else None
    
    if role != "farmer":
        return jsonify({"error": "Only farmers can reject orders"}), 403
    
    order = Order.query.get_or_404(order_id)
    
    if not any(i.farmer_id == user_id for i in order.items):
        return jsonify({"error": "Unauthorized"}), 403
    
    order.status = "rejected"
    db.session.commit()
    return jsonify({"message": "Order rejected"})


@orders_bp.route("/create", methods=["POST"])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or "items" not in data:
        return jsonify({"error": "No items provided"}), 400
    
    order = Order(buyer_id=user_id)
    db.session.add(order)
    
    for item_data in data["items"]:
        animal_id = item_data.get("animal_id")
        quantity = item_data.get("quantity", 1)
        
        order_item = OrderItem(
            order=order,
            animal_id=animal_id,
            farmer_id=1,  
            price=100.0 * quantity  
        )
        db.session.add(order_item)
    
    db.session.commit()
    return jsonify({"message": "Order created successfully", "order_id": order.id})
