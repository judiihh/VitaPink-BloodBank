from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.models import User, UserRole, user_schema
from app import db
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

# JWT blacklist for logout functionality
blacklisted_tokens = set()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.get_user_by_username(data['username']):
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.get_user_by_email(data['email']):
            return jsonify({'error': 'Email already exists'}), 409
        
        # Validate password strength (basic)
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Determine user role
        role = UserRole.DONOR  # Default role
        if data.get('role'):
            try:
                role = UserRole(data['role'])
            except ValueError:
                return jsonify({'error': 'Invalid role specified'}), 400
        
        # Create user
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
            'role': role
        }
        
        # Add optional fields
        optional_fields = ['first_name', 'last_name', 'phone_number', 'blood_type', 
                          'address', 'city', 'state', 'zip_code', 'country']
        for field in optional_fields:
            if data.get(field):
                user_data[field] = data[field]
        
        # Convert birth_date if provided
        if data.get('birth_date'):
            try:
                user_data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid birth_date format. Use YYYY-MM-DD'}), 400
        
        user = User.create_user(**user_data)
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role.value}
        )
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user_schema.dump(user)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return access token"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user by email
        user = User.get_user_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Verify password
        if not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role.value}
        )
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user by blacklisting the JWT token"""
    try:
        # Get the JWT token identifier
        jti = get_jwt()['jti']
        
        # Add token to blacklist
        blacklisted_tokens.add(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Fields that can be updated
        updatable_fields = ['first_name', 'last_name', 'phone_number', 'blood_type',
                           'address', 'city', 'state', 'zip_code', 'country']
        
        update_data = {}
        for field in updatable_fields:
            if field in data:
                update_data[field] = data[field]
        
        # Handle birth_date separately
        if 'birth_date' in data:
            try:
                update_data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid birth_date format. Use YYYY-MM-DD'}), 400
        
        # Update user
        user.update_user(**update_data)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Verify current password
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Validate new password
        if len(data['new_password']) < 6:
            return jsonify({'error': 'New password must be at least 6 characters long'}), 400
        
        # Update password
        user.update_password(data['new_password'])
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if token is valid and return user info"""
    try:
        user_id = get_jwt_identity()
        user = User.get_user_by_id(user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Invalid or inactive user'}), 401
        
        return jsonify({
            'valid': True,
            'user': user_schema.dump(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# JWT token blacklist checker
def check_if_token_revoked(jwt_header, jwt_payload):
    """Check if JWT token is in blacklist"""
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens 