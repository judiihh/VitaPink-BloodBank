from app import db, ma
from datetime import datetime
import bcrypt
from enum import Enum

class UserRole(Enum):
    DONOR = 'donor'
    ADMIN = 'admin'
    LAB = 'lab'

class User(db.Model):
    """User model for donors and administrators"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.DONOR)
    
    # Personal Information
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    birth_date = db.Column(db.Date)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
    
    # Address Information
    address = db.Column(db.String(500))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    
    # Account Status
    is_active = db.Column(db.Boolean, default=True)
    is_eligible = db.Column(db.Boolean, default=True)
    last_donation_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    donations = db.relationship('Donation', backref='donor', lazy=True)
    
    def __init__(self, username, email, password, role=UserRole.DONOR, **kwargs):
        """Initialize user with hashed password"""
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)
        self.role = role
        
        # Set additional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def update_password(self, new_password):
        """Update user password with new hash"""
        self.password_hash = self.hash_password(new_password)
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def create_user(cls, username, email, password, role=UserRole.DONOR, **kwargs):
        """Create new user"""
        user = cls(username=username, email=email, password=password, role=role, **kwargs)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def get_user_by_id(cls, user_id):
        """Get user by ID"""
        return cls.query.get(user_id)
    
    @classmethod
    def get_user_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_user_by_username(cls, username):
        """Get user by username"""
        return cls.query.filter_by(username=username).first()
    
    def update_user(self, **kwargs):
        """Update user information"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key != 'password_hash':
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def delete_user(self):
        """Soft delete user by setting is_active to False"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'blood_type': self.blood_type,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'country': self.country,
            'is_active': self.is_active,
            'is_eligible': self.is_eligible,
            'last_donation_date': self.last_donation_date.isoformat() if self.last_donation_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.username}>'

# Marshmallow Schema for serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('password_hash',)

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True) 