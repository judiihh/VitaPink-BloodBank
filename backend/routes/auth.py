from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models.user import User
from utils.validators import UserValidator, ValidationError
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract and validate all fields
        try:
            email = UserValidator.validate_email(data.get('email'))
            username = UserValidator.validate_username(data.get('username'))
            password = UserValidator.validate_password(data.get('password'))
            confirm_password = data.get('confirmPassword')
            
            # Check password confirmation
            if password != confirm_password:
                return jsonify({
                    'success': False,
                    'message': 'Passwords do not match'
                }), 400
            
            # Personal information
            first_name = UserValidator.validate_name(data.get('firstName'), 'First name')
            last_name = UserValidator.validate_name(data.get('lastName'), 'Last name')
            phone_number = UserValidator.validate_phone_number(data.get('phone'))
            birth_date = UserValidator.validate_birth_date(data.get('birthDate'))
            gender = UserValidator.validate_gender(data.get('gender'))
            blood_type = UserValidator.validate_blood_type(data.get('bloodType'))
            
            # Address information
            address = UserValidator.validate_address(data.get('address'))
            city = UserValidator.validate_city(data.get('city'))
            state = UserValidator.validate_state(data.get('state'))
            zip_code = UserValidator.validate_zip_code(data.get('zipCode'))
            country = UserValidator.validate_country(data.get('country'))
            
            # Donation information
            can_donate_now = data.get('canDonateNow', 'no') == 'yes'
            last_donation_date = None
            if data.get('lastDonationDate'):
                last_donation_date = UserValidator.validate_last_donation_date(data.get('lastDonationDate'))
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        # Check if user already exists
        if User.email_exists(email):
            return jsonify({
                'success': False,
                'message': 'Email address is already registered'
            }), 409
        
        if User.username_exists(username):
            return jsonify({
                'success': False,
                'message': 'Username is already taken'
            }), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=User.hash_password(password),
            role='donor',  # Default role
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            birth_date=birth_date,
            gender=gender,
            blood_type=blood_type,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            country=country,
            is_active=True,
            is_eligible=can_donate_now,
            last_donation_date=last_donation_date
        )
        
        # Save user to database
        user_id = user.save()
        
        if user_id:
            # Create JWT tokens (convert ID to string for JWT)
            access_token = create_access_token(identity=str(user_id))
            refresh_token = create_refresh_token(identity=str(user_id))
            
            return jsonify({
                'success': True,
                'message': 'Registration successful',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to create user account'
            }), 500
    
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during registration'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user by email
        user = User.find_by_email(email)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not User.verify_password(password, user.password_hash):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Account is deactivated. Please contact support.'
            }), 401
        
        # Create JWT tokens (convert ID to string for JWT)
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.find_by_id(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({
                'success': False,
                'message': 'Invalid user or account deactivated'
            }), 401
        
        new_access_token = create_access_token(identity=str(current_user_id))
        
        return jsonify({
            'success': True,
            'access_token': new_access_token
        }), 200
    
    except Exception as e:
        print(f"Token refresh error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during token refresh'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user's profile."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
    
    except Exception as e:
        print(f"Profile retrieval error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while retrieving profile'
        }), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user (client-side token removal)."""
    return jsonify({
        'success': True,
        'message': 'Logout successful. Please remove tokens from client.'
    }), 200 