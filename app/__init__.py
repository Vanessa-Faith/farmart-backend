from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.animals import animals_bp
    from app.routes.carts import carts_bp
    from app.routes.orders import orders_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(animals_bp, url_prefix='/api/animals')
    app.register_blueprint(carts_bp, url_prefix='/api/carts')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'Farmart API is running'}, 200
    
    return app
