from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.order import Order

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/orders/<int:order_id>/refund', methods=['POST'])
@jwt_required()
def refund_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != 'rejected':
        return jsonify({'message': 'Refund only allowed for rejected orders'}), 400
    order.status = 'refunded'
    db.session.commit()
    return jsonify(order.to_dict()), 200
