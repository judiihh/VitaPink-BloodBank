from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import BloodInventory, User, UserRole, inventory_schema, inventories_schema
from app import db
from functools import wraps

inventory_bp = Blueprint('inventory', __name__)

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

@inventory_bp.route('', methods=['GET'])
@jwt_required()
def get_inventory():
    """Get blood inventory - all users can view basic info"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        inventory_items = BloodInventory.get_all_stock()
        
        # Donors see limited information
        if current_user.role == UserRole.DONOR:
            limited_inventory = []
            for item in inventory_items:
                limited_data = {
                    'blood_type': item.blood_type,
                    'stock_status': item.get_stock_status(),
                    'is_low_stock': item.is_low_stock(),
                    'is_critical_stock': item.is_critical_stock(),
                    'last_updated': item.last_updated.isoformat()
                }
                limited_inventory.append(limited_data)
            
            return jsonify({
                'inventory': limited_inventory
            }), 200
        
        # Admins see full information
        return jsonify({
            'inventory': [item.to_dict() for item in inventory_items]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<blood_type>', methods=['GET'])
@jwt_required()
def get_inventory_by_blood_type(blood_type):
    """Get inventory for specific blood type"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate blood type
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_type not in valid_blood_types:
            return jsonify({'error': 'Invalid blood type'}), 400
        
        inventory_item = BloodInventory.get_stock_by_blood_type(blood_type)
        
        if not inventory_item:
            return jsonify({'error': 'Blood type not found in inventory'}), 404
        
        # Donors see limited information
        if current_user.role == UserRole.DONOR:
            limited_data = {
                'blood_type': inventory_item.blood_type,
                'stock_status': inventory_item.get_stock_status(),
                'is_low_stock': inventory_item.is_low_stock(),
                'is_critical_stock': inventory_item.is_critical_stock(),
                'last_updated': inventory_item.last_updated.isoformat()
            }
            return jsonify({'inventory': limited_data}), 200
        
        # Admins see full information
        return jsonify({
            'inventory': inventory_item.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<blood_type>', methods=['PUT'])
@admin_required
def update_inventory(blood_type):
    """Update blood inventory stock level (admin only)"""
    try:
        # Validate blood type
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_type not in valid_blood_types:
            return jsonify({'error': 'Invalid blood type'}), 400
        
        inventory_item = BloodInventory.get_stock_by_blood_type(blood_type)
        
        if not inventory_item:
            return jsonify({'error': 'Blood type not found in inventory'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if 'current_stock' not in data:
            return jsonify({'error': 'current_stock is required'}), 400
        
        try:
            new_stock = float(data['current_stock'])
            if new_stock < 0:
                return jsonify({'error': 'Stock cannot be negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid stock value'}), 400
        
        # Determine transaction type
        transaction_type = data.get('transaction_type', 'manual')
        
        # Update stock
        inventory_item.update_stock(new_stock, transaction_type)
        
        # Check for low stock and potentially trigger notifications
        if inventory_item.is_low_stock():
            # TODO: Implement push notification logic here
            pass
        
        return jsonify({
            'message': f'{blood_type} inventory updated successfully',
            'inventory': inventory_item.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<blood_type>/add', methods=['POST'])
@admin_required
def add_stock(blood_type):
    """Add stock to blood inventory (admin only)"""
    try:
        # Validate blood type
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_type not in valid_blood_types:
            return jsonify({'error': 'Invalid blood type'}), 400
        
        inventory_item = BloodInventory.get_stock_by_blood_type(blood_type)
        
        if not inventory_item:
            return jsonify({'error': 'Blood type not found in inventory'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if 'quantity' not in data:
            return jsonify({'error': 'quantity is required'}), 400
        
        try:
            quantity = float(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        # Determine transaction type
        transaction_type = data.get('transaction_type', 'donation')
        
        # Add stock
        inventory_item.add_stock(quantity, transaction_type)
        
        return jsonify({
            'message': f'Added {quantity}mL to {blood_type} inventory',
            'inventory': inventory_item.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/<blood_type>/remove', methods=['POST'])
@admin_required
def remove_stock(blood_type):
    """Remove stock from blood inventory (admin only)"""
    try:
        # Validate blood type
        valid_blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if blood_type not in valid_blood_types:
            return jsonify({'error': 'Invalid blood type'}), 400
        
        inventory_item = BloodInventory.get_stock_by_blood_type(blood_type)
        
        if not inventory_item:
            return jsonify({'error': 'Blood type not found in inventory'}), 404
        
        data = request.get_json()
        
        # Validate required fields
        if 'quantity' not in data:
            return jsonify({'error': 'quantity is required'}), 400
        
        try:
            quantity = float(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be positive'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid quantity value'}), 400
        
        # Determine transaction type
        transaction_type = data.get('transaction_type', 'dispensed')
        
        # Remove stock
        inventory_item.remove_stock(quantity, transaction_type)
        
        return jsonify({
            'message': f'Removed {quantity}mL from {blood_type} inventory',
            'inventory': inventory_item.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_inventory_alerts():
    """Get inventory alerts for low stock"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.get_user_by_id(current_user_id)
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get low stock alerts
        low_stock_items = BloodInventory.get_low_stock_alerts()
        critical_stock_items = BloodInventory.get_critical_stock_alerts()
        
        alerts = {
            'low_stock': [],
            'critical_stock': [],
            'total_alerts': len(low_stock_items) + len(critical_stock_items)
        }
        
        # Format alerts based on user role
        if current_user.role == UserRole.DONOR:
            # Donors see simplified alerts
            for item in low_stock_items:
                alerts['low_stock'].append({
                    'blood_type': item.blood_type,
                    'status': 'low',
                    'message': f'{item.blood_type} blood is running low. Consider donating!'
                })
            
            for item in critical_stock_items:
                alerts['critical_stock'].append({
                    'blood_type': item.blood_type,
                    'status': 'critical',
                    'message': f'{item.blood_type} blood is critically low. Urgent donations needed!'
                })
        else:
            # Admins see detailed alerts
            for item in low_stock_items:
                alerts['low_stock'].append({
                    'blood_type': item.blood_type,
                    'current_stock': float(item.current_stock),
                    'min_threshold': float(item.min_threshold),
                    'available_stock': float(item.get_available_stock()),
                    'status': 'low',
                    'last_updated': item.last_updated.isoformat()
                })
            
            for item in critical_stock_items:
                alerts['critical_stock'].append({
                    'blood_type': item.blood_type,
                    'current_stock': float(item.current_stock),
                    'min_threshold': float(item.min_threshold),
                    'available_stock': float(item.get_available_stock()),
                    'status': 'critical',
                    'last_updated': item.last_updated.isoformat()
                })
        
        return jsonify(alerts), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/initialize', methods=['POST'])
@admin_required
def initialize_inventory():
    """Initialize inventory with all blood types (admin only)"""
    try:
        BloodInventory.initialize_inventory()
        
        return jsonify({
            'message': 'Inventory initialized successfully for all blood types'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@inventory_bp.route('/stats', methods=['GET'])
@admin_required
def get_inventory_statistics():
    """Get inventory statistics (admin only)"""
    try:
        inventory_items = BloodInventory.get_all_stock()
        
        stats = {
            'total_blood_types': len(inventory_items),
            'total_stock': 0,
            'total_available_stock': 0,
            'total_reserved_stock': 0,
            'total_expired_stock': 0,
            'low_stock_count': 0,
            'critical_stock_count': 0,
            'blood_type_details': []
        }
        
        for item in inventory_items:
            stats['total_stock'] += float(item.current_stock)
            stats['total_available_stock'] += float(item.get_available_stock())
            stats['total_reserved_stock'] += float(item.reserved_stock)
            stats['total_expired_stock'] += float(item.expired_stock)
            
            if item.is_critical_stock():
                stats['critical_stock_count'] += 1
            elif item.is_low_stock():
                stats['low_stock_count'] += 1
            
            stats['blood_type_details'].append({
                'blood_type': item.blood_type,
                'current_stock': float(item.current_stock),
                'available_stock': float(item.get_available_stock()),
                'stock_status': item.get_stock_status(),
                'units_received_today': float(item.units_received_today),
                'units_dispensed_today': float(item.units_dispensed_today)
            })
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 