from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    jwt.init_app(app)
    
    from app.routes.auth import auth_bp
    from app.routes.orders import orders_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(orders_bp)
    
    @app.route('/')
    def index():
        return {"status": "running", "api": "/api/orders"}
    
    return app
