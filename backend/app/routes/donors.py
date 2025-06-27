from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import User, UserRole, user_schema, users_schema
from app import db
from functools import wraps

donors_bp = Blueprint('donors', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user or current_user.role not in [UserRole.ADMIN, UserRole.LAB]:
            return jsonify({'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function

@donors_bp.route('', methods=['GET'])
@admin_required
def get_all_donors():
    """Get all donors (admin only)"""
    try:
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        blood_type = request.args.get('blood_type')
        is_eligible = request.args.get('is_eligible')
        
        # Build query
        query = User.query.filter_by(role=UserRole.DONOR, is_active=True)
        
        # Apply filters
        if blood_type:
            query = query.filter_by(blood_type=blood_type)
        
        if is_eligible is not None:
            eligible_bool = is_eligible.lower() == 'true'
            query = query.filter_by(is_eligible=eligible_bool)
        
        # Paginate results
        donors = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'donors': users_schema.dump(donors.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': donors.total,
                'pages': donors.pages,
                'has_next': donors.has_next,
                'has_prev': donors.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/<int:donor_id>', methods=['GET'])
@jwt_required()
def get_donor_by_id(donor_id):
    """Get donor by ID (admin or self)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        # Check if user can access this donor's info
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            current_user_id != donor_id):
            return jsonify({'error': 'Access denied'}), 403
        
        donor = User.get_user_by_id(donor_id)
        
        if not donor:
            return jsonify({'error': 'Donor not found'}), 404
        
        if donor.role != UserRole.DONOR:
            return jsonify({'error': 'User is not a donor'}), 400
        
        return jsonify({
            'donor': user_schema.dump(donor)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/<int:donor_id>', methods=['PUT'])
@jwt_required()
def update_donor(donor_id):
    """Update donor information (admin or self)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        # Check if user can update this donor's info
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            current_user_id != donor_id):
            return jsonify({'error': 'Access denied'}), 403
        
        donor = User.get_user_by_id(donor_id)
        
        if not donor:
            return jsonify({'error': 'Donor not found'}), 404
        
        if donor.role != UserRole.DONOR:
            return jsonify({'error': 'User is not a donor'}), 400
        
        data = request.get_json()
        
        # Fields that can be updated
        updatable_fields = ['first_name', 'last_name', 'phone_number', 'blood_type',
                           'address', 'city', 'state', 'zip_code', 'country']
        
        # Admin can update additional fields
        if current_user.role in [UserRole.ADMIN, UserRole.LAB]:
            updatable_fields.extend(['is_eligible', 'last_donation_date'])
        
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                if field == 'last_donation_date' and data[field]:
                    try:
                        from datetime import datetime
                        update_data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                    except ValueError:
                        return jsonify({'error': 'Invalid last_donation_date format'}), 400
                else:
                    update_data[field] = data[field]
        
        # Handle birth_date separately
        if 'birth_date' in data:
            try:
                from datetime import datetime
                update_data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid birth_date format. Use YYYY-MM-DD'}), 400
        
        # Update donor
        donor.update_user(**update_data)
        
        return jsonify({
            'message': 'Donor updated successfully',
            'donor': user_schema.dump(donor)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/<int:donor_id>/deactivate', methods=['PUT'])
@admin_required
def deactivate_donor(donor_id):
    """Deactivate donor account (admin only)"""
    try:
        donor = User.get_user_by_id(donor_id)
        
        if not donor:
            return jsonify({'error': 'Donor not found'}), 404
        
        if donor.role != UserRole.DONOR:
            return jsonify({'error': 'User is not a donor'}), 400
        
        donor.delete_user()  # This sets is_active to False
        
        return jsonify({'message': 'Donor deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/<int:donor_id>/activate', methods=['PUT'])
@admin_required
def activate_donor(donor_id):
    """Activate donor account (admin only)"""
    try:
        donor = User.get_user_by_id(donor_id)
        
        if not donor:
            return jsonify({'error': 'Donor not found'}), 404
        
        if donor.role != UserRole.DONOR:
            return jsonify({'error': 'User is not a donor'}), 400
        
        donor.update_user(is_active=True)
        
        return jsonify({'message': 'Donor activated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/search', methods=['GET'])
@admin_required
def search_donors():
    """Search donors by various criteria (admin only)"""
    try:
        # Get search parameters
        search_term = request.args.get('q', '')
        blood_type = request.args.get('blood_type')
        city = request.args.get('city')
        state = request.args.get('state')
        is_eligible = request.args.get('is_eligible')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Build query
        query = User.query.filter_by(role=UserRole.DONOR, is_active=True)
        
        # Apply search filters
        if search_term:
            search_filter = (
                User.first_name.like(f'%{search_term}%') |
                User.last_name.like(f'%{search_term}%') |
                User.username.like(f'%{search_term}%') |
                User.email.like(f'%{search_term}%')
            )
            query = query.filter(search_filter)
        
        if blood_type:
            query = query.filter_by(blood_type=blood_type)
        
        if city:
            query = query.filter_by(city=city)
        
        if state:
            query = query.filter_by(state=state)
        
        if is_eligible is not None:
            eligible_bool = is_eligible.lower() == 'true'
            query = query.filter_by(is_eligible=eligible_bool)
        
        # Paginate results
        donors = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'donors': users_schema.dump(donors.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': donors.total,
                'pages': donors.pages,
                'has_next': donors.has_next,
                'has_prev': donors.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donors_bp.route('/stats', methods=['GET'])
@admin_required
def get_donor_statistics():
    """Get donor statistics (admin only)"""
    try:
        # Total donors
        total_donors = User.query.filter_by(role=UserRole.DONOR, is_active=True).count()
        
        # Eligible donors
        eligible_donors = User.query.filter_by(
            role=UserRole.DONOR, 
            is_active=True, 
            is_eligible=True
        ).count()
        
        # Donors by blood type
        blood_type_stats = {}
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for blood_type in blood_types:
            count = User.query.filter_by(
                role=UserRole.DONOR,
                is_active=True,
                blood_type=blood_type
            ).count()
            blood_type_stats[blood_type] = count
        
        # Recent registrations (last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_registrations = User.query.filter(
            User.role == UserRole.DONOR,
            User.is_active == True,
            User.created_at >= thirty_days_ago
        ).count()
        
        return jsonify({
            'total_donors': total_donors,
            'eligible_donors': eligible_donors,
            'ineligible_donors': total_donors - eligible_donors,
            'blood_type_distribution': blood_type_stats,
            'recent_registrations': recent_registrations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 