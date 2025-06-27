from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_name=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.donors import donors_bp
    from app.routes.inventory import inventory_bp
    from app.routes.donations import donations_bp
    from app.routes.locations import locations_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(donors_bp, url_prefix='/api/donors')
    app.register_blueprint(inventory_bp, url_prefix='/api/inventory')
    app.register_blueprint(donations_bp, url_prefix='/api/donations')
    app.register_blueprint(locations_bp, url_prefix='/api/locations')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 