import os
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing config
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager
from app.models import db
from app.routes.orders import orders_bp
from config import config


def create_app(config_name=None):
    """Application factory function"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(orders_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'message': 'FarmArt Backend API',
            'version': '1.0',
            'endpoints': {
                'orders': '/api/orders'
            }
        }
    
    # Register error handlers
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    """Register custom error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
