import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(app, origins=app.config['CORS_ORIGINS'])
    jwt = JWTManager(app)
    
    # JWT error handlers for debugging
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"JWT Error: Token expired - {jwt_payload}")
        return jsonify({'message': 'Token has expired'}), 422
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"JWT Error: Invalid token - {error}")
        return jsonify({'message': 'Invalid token'}), 422
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"JWT Error: Missing token - {error}")
        return jsonify({'message': 'Authorization token is required'}), 422
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'message': 'VitaPink BloodBank API is running',
            'version': '1.0.0'
        }
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'message': 'VitaPink BloodBank API',
            'version': '1.0.0',
            'status': 'active',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'health': '/health'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"Starting VitaPink BloodBank API...")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    
    app.run(host=host, port=port, debug=True) 