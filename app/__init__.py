from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config
import os

db = SQLAlchemy()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    JWTManager(app)
    CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
    
    from app.routes.auth import auth_bp
    from app.routes.animals import animals_bp
    from app.routes.orders import orders_bp
    from app.routes.carts import carts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(animals_bp, url_prefix='/api/animals')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(carts_bp, url_prefix='/api/carts')
    
    with app.app_context():
        db.create_all()
    
    register_error_handlers(app)
    
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
