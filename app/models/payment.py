from app import db
from datetime import datetime


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    provider = db.Column(db.String(50))  # 'stripe', 'paypal', 'mock', etc.
    provider_transaction_id = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'succeeded', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert payment to dictionary"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': float(self.amount) if self.amount else None,
            'provider': self.provider,
            'provider_transaction_id': self.provider_transaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id}>'
