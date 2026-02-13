# app/_init_.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Config
    app.config['JWT_SECRET_KEY'] = os.getenv("SECRET_KEY", "super-secret")  # use .env or Render secrets
    JWTManager(app)

    # Import blueprints
    from app.routes.animals import animals_bp
    from app.routes.auth import auth_bp
    from app.routes.orders import orders_bp

    # Register blueprints
    app.register_blueprint(animals_bp, url_prefix="/api/animals")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    return app