from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from marshmallow import Schema, fields, ValidationError

auth_bp = Blueprint('auth', __name__)

class UserRegistrationSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    user_type = fields.Str(required=True, validate=lambda x: x in ['farmer', 'user'])
    phone = fields.Str()
    county = fields.Str()

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        validated_data = registration_schema.load(data)
        
        if User.query.filter_by(email=validated_data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            user_type=validated_data['user_type'],
            phone=validated_data.get('phone'),
            county=validated_data.get('county')
        )
        user.set_password(validated_data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type
            }
        }), 201
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        validated_data = login_schema.load(data)
        
        user = User.query.filter_by(email=validated_data['email']).first()
        
        if not user or not user.check_password(validated_data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'user_type': user.user_type
            }
        }), 200
        
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
    except Exception as e:
        return jsonify({'error': 'Login failed'}), 500