import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vitapink-bloodbank-secret-key-2025'
    
    # Database Configuration
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_PORT = int(os.environ.get('DB_PORT') or 3306)
    DB_NAME = os.environ.get('DB_NAME') or 'vitapink_bloodbank'
    DB_USER = os.environ.get('DB_USER') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'admin'
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'vitapink-jwt-secret-2025'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Application Configuration
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 