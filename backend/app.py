from app import create_app
from app.models import BloodInventory
import os

# Create Flask application
app = create_app()

@app.before_first_request
def initialize_database():
    """Initialize database with default data"""
    try:
        # Initialize blood inventory with all blood types
        BloodInventory.initialize_inventory()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.route('/')
def index():
    """Root endpoint"""
    return {
        'message': 'VitaPink BloodBank API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'auth': '/api/auth',
            'donors': '/api/donors',
            'inventory': '/api/inventory',
            'donations': '/api/donations',
            'locations': '/api/locations'
        }
    }

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': str(app.config.get('JWT_ACCESS_TOKEN_EXPIRES')),
        'database': 'connected'
    }

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    print(f"Starting VitaPink BloodBank API...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    
    app.run(host=host, port=port, debug=debug) 