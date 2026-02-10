from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
import re

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user (farmer or buyer)
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'message': f'{field} is required'}), 400
    
    # Validate email format
    if not validate_email(data.get('email')):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Validate password length
    if len(data.get('password')) < 6:
        return jsonify({'message': 'Password must be at least 6 characters'}), 400
    
    # Validate role
    role = data.get('role', 'buyer')
    if role not in ['farmer', 'buyer']:
        return jsonify({'message': 'Role must be either farmer or buyer'}), 400
    
    # Check if email already exists
    existing_user = User.query.filter_by(email=data.get('email')).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 409
    
    # Create new user
    try:
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            role=role
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    """
    data = request.get_json()
    
    # Validate required fields
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Email and password are required'}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data.get('email')).first()
    
    # Verify user exists and password is correct
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if not user.check_password(data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get user', 'error': str(e)}), 500
