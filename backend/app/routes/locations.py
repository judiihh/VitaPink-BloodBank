from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Location, User, UserRole, location_schema, locations_schema
from app import db
from functools import wraps

locations_bp = Blueprint('locations', __name__)

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

@locations_bp.route('', methods=['GET'])
def get_all_locations():
    """Get all active donation locations - public endpoint"""
    try:
        # Get query parameters
        location_type = request.args.get('type')
        accepting_donations = request.args.get('accepting_donations')
        search = request.args.get('search')
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', type=float)
        
        # Build query
        query = Location.query.filter_by(is_active=True)
        
        # Apply filters
        if location_type:
            query = query.filter_by(location_type=location_type)
        
        if accepting_donations is not None:
            accepting_bool = accepting_donations.lower() == 'true'
            query = query.filter_by(is_accepting_donations=accepting_bool)
        
        if search:
            search_filter = (
                Location.name.like(f'%{search}%') |
                Location.address.like(f'%{search}%') |
                Location.city.like(f'%{search}%')
            )
            query = query.filter(search_filter)
        
        locations = query.all()
        
        # Calculate distances if user location provided
        locations_data = []
        for location in locations:
            location_dict = location.to_dict()
            
            if lat and lng and location.latitude and location.longitude:
                distance = location.calculate_distance(lat, lng)
                if distance is not None:
                    location_dict['distance_km'] = distance
                    
                    # Filter by radius if specified
                    if radius and distance > radius:
                        continue
            
            locations_data.append(location_dict)
        
        # Sort by distance if available
        if lat and lng:
            locations_data.sort(key=lambda x: x.get('distance_km', float('inf')))
        
        return jsonify({
            'locations': locations_data,
            'total': len(locations_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location_by_id(location_id):
    """Get location by ID - public endpoint"""
    try:
        location = Location.get_location_by_id(location_id)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        if not location.is_active:
            return jsonify({'error': 'Location is not active'}), 404
        
        return jsonify({
            'location': location.to_dict(include_stats=True)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locations_bp.route('', methods=['POST'])
@admin_required
def create_location():
    """Create a new donation location (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create location
        location_data = {
            'name': data['name'],
            'address': data['address']
        }
        
        # Add optional fields
        optional_fields = [
            'latitude', 'longitude', 'contact_info', 'phone_number', 'email', 'website',
            'location_type', 'capacity', 'amenities', 'languages_spoken',
            'is_accepting_donations', 'appointments_required',
            'monday_open', 'monday_close', 'tuesday_open', 'tuesday_close',
            'wednesday_open', 'wednesday_close', 'thursday_open', 'thursday_close',
            'friday_open', 'friday_close', 'saturday_open', 'saturday_close',
            'sunday_open', 'sunday_close'
        ]
        
        for field in optional_fields:
            if field in data:
                # Handle time fields
                if field.endswith('_open') or field.endswith('_close'):
                    if data[field]:
                        try:
                            from datetime import datetime
                            time_obj = datetime.strptime(data[field], '%H:%M').time()
                            location_data[field] = time_obj
                        except ValueError:
                            return jsonify({'error': f'Invalid time format for {field}. Use HH:MM'}), 400
                else:
                    location_data[field] = data[field]
        
        location = Location.add_location(**location_data)
        
        return jsonify({
            'message': 'Location created successfully',
            'location': location.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>', methods=['PUT'])
@admin_required
def update_location(location_id):
    """Update location information (admin only)"""
    try:
        location = Location.get_location_by_id(location_id)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        data = request.get_json()
        
        # Fields that can be updated
        updatable_fields = [
            'name', 'address', 'latitude', 'longitude', 'contact_info', 'phone_number',
            'email', 'website', 'location_type', 'capacity', 'amenities', 'languages_spoken',
            'is_accepting_donations', 'appointments_required', 'current_wait_time',
            'monday_open', 'monday_close', 'tuesday_open', 'tuesday_close',
            'wednesday_open', 'wednesday_close', 'thursday_open', 'thursday_close',
            'friday_open', 'friday_close', 'saturday_open', 'saturday_close',
            'sunday_open', 'sunday_close'
        ]
        
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                # Handle time fields
                if field.endswith('_open') or field.endswith('_close'):
                    if data[field]:
                        try:
                            from datetime import datetime
                            time_obj = datetime.strptime(data[field], '%H:%M').time()
                            update_data[field] = time_obj
                        except ValueError:
                            return jsonify({'error': f'Invalid time format for {field}. Use HH:MM'}), 400
                    else:
                        update_data[field] = None
                else:
                    update_data[field] = data[field]
        
        # Update location
        location.update_location(**update_data)
        
        return jsonify({
            'message': 'Location updated successfully',
            'location': location.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>/deactivate', methods=['PUT'])
@admin_required
def deactivate_location(location_id):
    """Deactivate location (admin only)"""
    try:
        location = Location.get_location_by_id(location_id)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        location.deactivate_location()
        
        return jsonify({'message': 'Location deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>/activate', methods=['PUT'])
@admin_required
def activate_location(location_id):
    """Activate location (admin only)"""
    try:
        location = Location.get_location_by_id(location_id)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        location.activate_location()
        
        return jsonify({'message': 'Location activated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/<int:location_id>/wait-time', methods=['PUT'])
@jwt_required()
def update_wait_time(location_id):
    """Update location wait time"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        location = Location.get_location_by_id(location_id)
        
        if not location:
            return jsonify({'error': 'Location not found'}), 404
        
        data = request.get_json()
        
        if 'wait_time' not in data:
            return jsonify({'error': 'wait_time is required'}), 400
        
        try:
            wait_time = int(data['wait_time'])
            if wait_time < 0:
                return jsonify({'error': 'Wait time cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid wait time value'}), 400
        
        location.update_wait_time(wait_time)
        
        return jsonify({
            'message': 'Wait time updated successfully',
            'location': {
                'id': location.id,
                'name': location.name,
                'current_wait_time': location.current_wait_time
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/nearby', methods=['GET'])
def get_nearby_locations():
    """Get nearby locations based on user coordinates"""
    try:
        # Get coordinates from query parameters
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 50, type=float)  # Default 50km radius
        limit = request.args.get('limit', 10, type=int)  # Default 10 locations
        
        if not lat or not lng:
            return jsonify({'error': 'lat and lng parameters are required'}), 400
        
        # Get all active locations
        locations = Location.get_locations_accepting_donations()
        
        # Calculate distances and filter by radius
        nearby_locations = []
        for location in locations:
            if location.latitude and location.longitude:
                distance = location.calculate_distance(lat, lng)
                if distance is not None and distance <= radius:
                    location_dict = location.to_dict()
                    location_dict['distance_km'] = distance
                    nearby_locations.append(location_dict)
        
        # Sort by distance and limit results
        nearby_locations.sort(key=lambda x: x['distance_km'])
        nearby_locations = nearby_locations[:limit]
        
        return jsonify({
            'locations': nearby_locations,
            'total': len(nearby_locations),
            'search_params': {
                'latitude': lat,
                'longitude': lng,
                'radius_km': radius,
                'limit': limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/search', methods=['GET'])
def search_locations():
    """Search locations by name or address"""
    try:
        search_term = request.args.get('q', '')
        
        if not search_term or len(search_term) < 2:
            return jsonify({'error': 'Search term must be at least 2 characters'}), 400
        
        locations = Location.search_locations_by_name(search_term)
        
        return jsonify({
            'locations': [location.to_dict() for location in locations],
            'total': len(locations),
            'search_term': search_term
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@locations_bp.route('/types', methods=['GET'])
def get_location_types():
    """Get available location types"""
    return jsonify({
        'location_types': [
            {'value': 'blood_bank', 'label': 'Blood Bank'},
            {'value': 'hospital', 'label': 'Hospital'},
            {'value': 'mobile_unit', 'label': 'Mobile Unit'},
            {'value': 'community_center', 'label': 'Community Center'},
            {'value': 'clinic', 'label': 'Clinic'},
            {'value': 'university', 'label': 'University'},
            {'value': 'corporate', 'label': 'Corporate Location'}
        ]
    }), 200

@locations_bp.route('/stats', methods=['GET'])
@admin_required
def get_location_statistics():
    """Get location statistics (admin only)"""
    try:
        # Total locations
        total_locations = Location.query.filter_by(is_active=True).count()
        
        # Accepting donations
        accepting_donations = Location.query.filter_by(
            is_active=True,
            is_accepting_donations=True
        ).count()
        
        # By type
        type_stats = {}
        location_types = ['blood_bank', 'hospital', 'mobile_unit', 'community_center', 'clinic']
        
        for loc_type in location_types:
            count = Location.query.filter_by(
                is_active=True,
                location_type=loc_type
            ).count()
            type_stats[loc_type] = count
        
        # Average wait time
        avg_wait_time = db.session.query(db.func.avg(Location.current_wait_time)).filter(
            Location.is_active == True,
            Location.current_wait_time > 0
        ).scalar() or 0
        
        # Locations with appointments required
        appointments_required = Location.query.filter_by(
            is_active=True,
            appointments_required=True
        ).count()
        
        return jsonify({
            'total_locations': total_locations,
            'accepting_donations': accepting_donations,
            'not_accepting_donations': total_locations - accepting_donations,
            'location_type_breakdown': type_stats,
            'average_wait_time_minutes': round(float(avg_wait_time), 1),
            'appointments_required_count': appointments_required,
            'walk_in_available_count': total_locations - appointments_required
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 