from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Donation, DonationStatus, User, UserRole, BloodInventory, donation_schema, donations_schema
from app import db
from datetime import datetime, timedelta
from functools import wraps

donations_bp = Blueprint('donations', __name__)

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

@donations_bp.route('', methods=['GET'])
@jwt_required()
def get_donations():
    """Get donations - users see their own, admins see all"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        blood_type = request.args.get('blood_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build base query
        if current_user.role in [UserRole.ADMIN, UserRole.LAB]:
            # Admins can see all donations
            query = Donation.query
        else:
            # Donors can only see their own donations
            query = Donation.query.filter_by(user_id=current_user_id)
        
        # Apply filters
        if status:
            try:
                status_enum = DonationStatus(status)
                query = query.filter_by(status=status_enum)
            except ValueError:
                return jsonify({'error': 'Invalid status'}), 400
        
        if blood_type:
            valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            if blood_type not in valid_blood_types:
                return jsonify({'error': 'Invalid blood type'}), 400
            query = query.filter_by(blood_type=blood_type)
        
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d')
                query = query.filter(Donation.donation_date >= start_dt)
            except ValueError:
                return jsonify({'error': 'Invalid start_date format. Use YYYY-MM-DD'}), 400
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d')
                # Include the entire end date
                end_dt = end_dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Donation.donation_date <= end_dt)
            except ValueError:
                return jsonify({'error': 'Invalid end_date format. Use YYYY-MM-DD'}), 400
        
        # Order by donation date (most recent first)
        query = query.order_by(Donation.donation_date.desc())
        
        # Paginate results
        donations_page = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'donations': donations_schema.dump(donations_page.items),
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': donations_page.total,
                'pages': donations_page.pages,
                'has_next': donations_page.has_next,
                'has_prev': donations_page.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('', methods=['POST'])
@jwt_required()
def record_donation():
    """Record a new donation"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['blood_type', 'quantity', 'donation_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate blood type
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if data['blood_type'] not in valid_blood_types:
            return jsonify({'error': 'Invalid blood type'}), 400
        
        # Validate quantity
        try:
            quantity = float(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        # Parse donation date
        try:
            donation_date = datetime.fromisoformat(data['donation_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid donation_date format'}), 400
        
        # Determine user_id (admins can record for others)
        donor_id = current_user_id
        if current_user.role in [UserRole.ADMIN, UserRole.LAB] and data.get('user_id'):
            donor_id = data['user_id']
            
            # Verify the target user exists and is a donor
            target_user = User.get_user_by_id(donor_id)
            if not target_user or target_user.role != UserRole.DONOR:
                return jsonify({'error': 'Invalid donor user'}), 400
        
        # Create donation record
        donation_data = {
            'user_id': donor_id,
            'blood_type': data['blood_type'],
            'quantity': quantity,
            'donation_date': donation_date,
            'location_id': data.get('location_id'),
            'status': DonationStatus.PENDING
        }
        
        # Add optional medical data
        optional_fields = ['hemoglobin_level', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                          'weight', 'temperature', 'processing_notes']
        for field in optional_fields:
            if data.get(field):
                donation_data[field] = data[field]
        
        donation = Donation.record_donation(**donation_data)
        
        return jsonify({
            'message': 'Donation recorded successfully',
            'donation': donation_schema.dump(donation)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>', methods=['GET'])
@jwt_required()
def get_donation_by_id(donation_id):
    """Get donation by ID"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        donation = Donation.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check access permissions
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            donation.user_id != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        return jsonify({
            'donation': donation_schema.dump(donation)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>', methods=['PUT'])
@jwt_required()
def update_donation(donation_id):
    """Update donation information"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        donation = Donation.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check access permissions
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            donation.user_id != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Fields that can be updated
        updatable_fields = ['hemoglobin_level', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                           'weight', 'temperature', 'processing_notes']
        
        # Admins can update additional fields
        if current_user.role in [UserRole.ADMIN, UserRole.LAB]:
            updatable_fields.extend(['status', 'collection_bag_number', 'expiry_date'])
        
        update_data = {}
        
        for field in updatable_fields:
            if field in data:
                if field == 'status':
                    try:
                        update_data[field] = DonationStatus(data[field])
                    except ValueError:
                        return jsonify({'error': 'Invalid status'}), 400
                elif field == 'expiry_date' and data[field]:
                    try:
                        update_data[field] = datetime.fromisoformat(data[field].replace('Z', '+00:00'))
                    except ValueError:
                        return jsonify({'error': 'Invalid expiry_date format'}), 400
                else:
                    update_data[field] = data[field]
        
        # Update donation
        donation.update_donation(**update_data)
        
        return jsonify({
            'message': 'Donation updated successfully',
            'donation': donation_schema.dump(donation)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>/complete', methods=['POST'])
@admin_required
def complete_donation(donation_id):
    """Complete a donation and update inventory (admin only)"""
    try:
        donation = Donation.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        if donation.status == DonationStatus.COMPLETED:
            return jsonify({'error': 'Donation is already completed'}), 400
        
        data = request.get_json() or {}
        
        # Complete the donation
        donation.complete_donation(
            collection_bag_number=data.get('collection_bag_number'),
            expiry_date=datetime.fromisoformat(data['expiry_date'].replace('Z', '+00:00')) if data.get('expiry_date') else None
        )
        
        # Update blood inventory
        try:
            inventory_item = BloodInventory.get_stock_by_blood_type(donation.blood_type)
            if inventory_item:
                inventory_item.add_stock(float(donation.quantity), 'donation')
            
            # Update donor's last donation date
            donor = User.get_user_by_id(donation.user_id)
            if donor:
                donor.update_user(last_donation_date=donation.donation_date)
        
        except Exception as inventory_error:
            # Log error but don't fail the donation completion
            print(f"Error updating inventory: {inventory_error}")
        
        return jsonify({
            'message': 'Donation completed successfully',
            'donation': donation_schema.dump(donation)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/<int:donation_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_donation(donation_id):
    """Cancel a donation"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        donation = Donation.query.get(donation_id)
        
        if not donation:
            return jsonify({'error': 'Donation not found'}), 404
        
        # Check access permissions
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            donation.user_id != current_user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        if donation.status == DonationStatus.COMPLETED:
            return jsonify({'error': 'Cannot cancel completed donation'}), 400
        
        data = request.get_json() or {}
        reason = data.get('reason', 'Cancelled by user')
        
        # Cancel the donation
        donation.cancel_donation(reason)
        
        return jsonify({
            'message': 'Donation cancelled successfully',
            'donation': donation_schema.dump(donation)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_donations(user_id):
    """Get donations for a specific user"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check access permissions
        if (current_user.role not in [UserRole.ADMIN, UserRole.LAB] and 
            current_user_id != user_id):
            return jsonify({'error': 'Access denied'}), 403
        
        # Verify target user exists
        target_user = User.get_user_by_id(user_id)
        if not target_user:
            return jsonify({'error': 'User not found'}), 404
        
        donations = Donation.get_donations_by_user(user_id)
        
        return jsonify({
            'donations': donations_schema.dump(donations),
            'user': {
                'id': target_user.id,
                'username': target_user.username,
                'blood_type': target_user.blood_type
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@donations_bp.route('/stats', methods=['GET'])
@admin_required
def get_donation_statistics():
    """Get donation statistics (admin only)"""
    try:
        # Get date range (default to last 30 days)
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        if request.args.get('start_date'):
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        
        if request.args.get('end_date'):
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)
        
        # Get donations in date range
        donations_query = Donation.query.filter(
            Donation.donation_date >= start_date,
            Donation.donation_date <= end_date
        )
        
        total_donations = donations_query.count()
        completed_donations = donations_query.filter_by(status=DonationStatus.COMPLETED).count()
        pending_donations = donations_query.filter_by(status=DonationStatus.PENDING).count()
        cancelled_donations = donations_query.filter_by(status=DonationStatus.CANCELLED).count()
        
        # Calculate total volume
        completed_query = donations_query.filter_by(status=DonationStatus.COMPLETED)
        total_volume = db.session.query(db.func.sum(Donation.quantity)).filter(
            Donation.donation_date >= start_date,
            Donation.donation_date <= end_date,
            Donation.status == DonationStatus.COMPLETED
        ).scalar() or 0
        
        # Donations by blood type
        blood_type_stats = {}
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for blood_type in blood_types:
            count = completed_query.filter_by(blood_type=blood_type).count()
            volume = db.session.query(db.func.sum(Donation.quantity)).filter(
                Donation.donation_date >= start_date,
                Donation.donation_date <= end_date,
                Donation.status == DonationStatus.COMPLETED,
                Donation.blood_type == blood_type
            ).scalar() or 0
            
            blood_type_stats[blood_type] = {
                'count': count,
                'volume': float(volume)
            }
        
        return jsonify({
            'period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat()
            },
            'total_donations': total_donations,
            'completed_donations': completed_donations,
            'pending_donations': pending_donations,
            'cancelled_donations': cancelled_donations,
            'total_volume_ml': float(total_volume),
            'blood_type_breakdown': blood_type_stats,
            'completion_rate': round((completed_donations / total_donations * 100) if total_donations > 0 else 0, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 