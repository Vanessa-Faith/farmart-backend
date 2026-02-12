import os
from dotenv import load_dotenv

# Load environment variables from .env file BEFORE importing config
load_dotenv()

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    JWTManager(app)
    CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:5174'])
    
    from app.routes.auth import auth_bp
    from app.routes.animals import animals_bp
    from app.routes.orders import orders_bp
    from app.routes.carts import carts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(animals_bp, url_prefix='/api/animals')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(carts_bp, url_prefix='/api/carts')
    
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
    
    register_error_handlers(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_error_handlers(app):
    
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400
