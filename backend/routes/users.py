from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from utils.validators import UserValidator, ValidationError

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Update allowed fields
        try:
            if 'firstName' in data:
                user.first_name = UserValidator.validate_name(data['firstName'], 'First name')
            
            if 'lastName' in data:
                user.last_name = UserValidator.validate_name(data['lastName'], 'Last name')
            
            if 'phone' in data:
                user.phone_number = UserValidator.validate_phone_number(data['phone'])
            
            if 'address' in data:
                user.address = UserValidator.validate_address(data['address'])
            
            if 'city' in data:
                user.city = UserValidator.validate_city(data['city'])
            
            if 'state' in data:
                user.state = UserValidator.validate_state(data['state'])
            
            if 'zipCode' in data:
                user.zip_code = UserValidator.validate_zip_code(data['zipCode'])
            
            if 'country' in data:
                user.country = UserValidator.validate_country(data['country'])
            
            if 'lastDonationDate' in data and data['lastDonationDate']:
                user.last_donation_date = UserValidator.validate_last_donation_date(data['lastDonationDate'])
            
        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        # Save updated user
        if user.save():
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to update profile'
            }), 500
    
    except Exception as e:
        print(f"Profile update error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while updating profile'
        }), 500

@users_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Change user password."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')
        
        if not all([current_password, new_password, confirm_password]):
            return jsonify({
                'success': False,
                'message': 'All password fields are required'
            }), 400
        
        # Verify current password
        if not User.verify_password(current_password, user.password_hash):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        # Validate new password
        try:
            UserValidator.validate_password(new_password)
        except ValidationError as e:
            return jsonify({
                'success': False,
                'message': str(e)
            }), 400
        
        # Check password confirmation
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'message': 'New passwords do not match'
            }), 400
        
        # Update password
        user.password_hash = User.hash_password(new_password)
        
        if user.save():
            return jsonify({
                'success': True,
                'message': 'Password changed successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to change password'
            }), 500
    
    except Exception as e:
        print(f"Password change error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while changing password'
        }), 500

@users_bp.route('/deactivate', methods=['PUT'])
@jwt_required()
def deactivate_account():
    """Deactivate user account."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        user = User.find_by_id(current_user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        user.is_active = False
        
        if user.save():
            return jsonify({
                'success': True,
                'message': 'Account deactivated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to deactivate account'
            }), 500
    
    except Exception as e:
        print(f"Account deactivation error: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred while deactivating account'
        }), 500

@users_bp.route('/eligibility', methods=['PUT'])
@jwt_required()
def update_eligibility():
    """Update donation eligibility status (is_active field)."""
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        print(f"Updating eligibility for user ID: {current_user_id}")
        
        user = User.find_by_id(current_user_id)
        
        if not user:
            print(f"User not found for ID: {current_user_id}")
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        print(f"Received data: {data}")
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        is_eligible = data.get('isEligible')
        print(f"isEligible value: {is_eligible}, type: {type(is_eligible)}")
        
        if is_eligible is None:
            return jsonify({
                'success': False,
                'message': 'Active status is required'
            }), 422
        
        # Update is_active instead of is_eligible since this represents donation availability
        old_status = user.is_active
        user.is_active = bool(is_eligible)
        print(f"Updating is_active from {old_status} to {user.is_active}")
        
        if user.save():
            print("User saved successfully")
            return jsonify({
                'success': True,
                'message': 'Active status updated successfully',
                'user': user.to_dict()
            }), 200
        else:
            print("Failed to save user")
            return jsonify({
                'success': False,
                'message': 'Failed to update active status'
            }), 500
    
    except Exception as e:
        print(f"Active status update error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'An error occurred while updating active status: {str(e)}'
        }), 500

@users_bp.route('/active-status', methods=['PUT'])
@jwt_required()
def update_active_status():
    """Update user's active donation status."""
    print("=== ACTIVE STATUS ENDPOINT HIT ===")
    try:
        current_user_id = int(get_jwt_identity())  # Convert string back to int
        print(f"Updating active status for user ID: {current_user_id}")
        
        user = User.find_by_id(current_user_id)
        
        if not user:
            print(f"User not found for ID: {current_user_id}")
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Debug request information
        print(f"Request content type: {request.content_type}")
        print(f"Request data (raw): {request.data}")
        print(f"Request form: {request.form}")
        print(f"Request json: {request.json}")
        
        data = request.get_json()
        print(f"Received data: {data}")
        print(f"Data type: {type(data)}")
        
        if not data:
            print("No data provided - returning 400")
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        is_active = data.get('isActive')
        print(f"isActive value: {is_active}, type: {type(is_active)}")
        
        if is_active is None:
            print("isActive is None - returning 422")
            print(f"Available keys in data: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")
            return jsonify({
                'success': False,
                'message': 'Active status is required'
            }), 422
        
        old_status = user.is_active
        user.is_active = bool(is_active)
        print(f"Updating is_active from {old_status} to {user.is_active}")
        
        if user.save():
            print("User saved successfully")
            return jsonify({
                'success': True,
                'message': 'Active status updated successfully',
                'user': user.to_dict()
            }), 200
        else:
            print("Failed to save user")
            return jsonify({
                'success': False,
                'message': 'Failed to update active status'
            }), 500
    
    except Exception as e:
        print(f"Active status update error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'An error occurred while updating active status: {str(e)}'
        }), 500 