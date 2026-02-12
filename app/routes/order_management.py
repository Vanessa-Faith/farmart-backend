from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import db
from app.models.order import Order
from app.utils.notification import send_notification  # Optional: for notifications


order_management_bp = Blueprint('order_management_bp', __name__)

@order_management_bp.route('/orders/<int:order_id>/accept', methods=['PATCH'])
@jwt_required()
def accept_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    if order.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    order.status = 'accepted'
    db.session.commit()
    # send_notification(order.buyer_id, "Order accepted!")  # Optional
    return jsonify({'message': 'Order accepted', 'order': order.serialize()}), 200

@order_management_bp.route('/orders/<int:order_id>/reject', methods=['PATCH'])
@jwt_required()
def reject_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    if order.farmer_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    order.status = 'rejected'
    db.session.commit()
    # send_notification(order.buyer_id, "Order rejected.")  # Optional
    # TODO: Trigger refund logic here
    return jsonify({'message': 'Order rejected', 'order': order.serialize()}), 200

