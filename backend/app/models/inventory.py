from app import db, ma
from datetime import datetime

class BloodInventory(db.Model):
    """Blood inventory model for tracking blood stock levels"""
    __tablename__ = 'blood_inventory'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), unique=True, nullable=False)
    current_stock = db.Column(db.Decimal(10, 2), nullable=False, default=0)  # in mL
    min_threshold = db.Column(db.Decimal(10, 2), default=1000)  # Minimum stock level in mL
    max_capacity = db.Column(db.Decimal(10, 2), default=10000)  # Maximum storage capacity in mL
    
    # Additional inventory information
    reserved_stock = db.Column(db.Decimal(10, 2), default=0)  # Stock reserved for specific purposes
    expired_stock = db.Column(db.Decimal(10, 2), default=0)  # Expired units awaiting disposal
    units_dispensed_today = db.Column(db.Decimal(10, 2), default=0)
    units_received_today = db.Column(db.Decimal(10, 2), default=0)
    
    # Tracking information
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_donation_date = db.Column(db.DateTime)
    last_dispensed_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, blood_type, current_stock=0, min_threshold=1000, **kwargs):
        """Initialize blood inventory record"""
        self.blood_type = blood_type
        self.current_stock = current_stock
        self.min_threshold = min_threshold
        
        # Set additional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def initialize_inventory(cls):
        """Initialize inventory with all blood types"""
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for blood_type in blood_types:
            existing = cls.query.filter_by(blood_type=blood_type).first()
            if not existing:
                inventory = cls(blood_type=blood_type)
                db.session.add(inventory)
        
        db.session.commit()
    
    @classmethod
    def get_stock_by_blood_type(cls, blood_type):
        """Get stock information for a specific blood type"""
        return cls.query.filter_by(blood_type=blood_type).first()
    
    @classmethod
    def get_all_stock(cls):
        """Get all blood inventory records"""
        return cls.query.all()
    
    @classmethod
    def get_low_stock_alerts(cls):
        """Get blood types with stock below minimum threshold"""
        return cls.query.filter(cls.current_stock <= cls.min_threshold).all()
    
    @classmethod
    def get_critical_stock_alerts(cls):
        """Get blood types with critically low stock (less than 50% of threshold)"""
        return cls.query.filter(cls.current_stock <= (cls.min_threshold * 0.5)).all()
    
    def update_stock(self, new_stock, transaction_type='manual'):
        """Update stock level"""
        old_stock = self.current_stock
        self.current_stock = new_stock
        self.last_updated = datetime.utcnow()
        
        # Update daily counters based on transaction type
        if transaction_type == 'donation':
            self.units_received_today += (new_stock - old_stock)
            self.last_donation_date = datetime.utcnow()
        elif transaction_type == 'dispensed':
            self.units_dispensed_today += (old_stock - new_stock)
            self.last_dispensed_date = datetime.utcnow()
        
        db.session.commit()
        return self
    
    def add_stock(self, quantity, transaction_type='donation'):
        """Add stock to current inventory"""
        new_stock = self.current_stock + quantity
        if new_stock > self.max_capacity:
            raise ValueError(f"Adding {quantity}mL would exceed maximum capacity of {self.max_capacity}mL")
        
        return self.update_stock(new_stock, transaction_type)
    
    def remove_stock(self, quantity, transaction_type='dispensed'):
        """Remove stock from current inventory"""
        new_stock = self.current_stock - quantity
        if new_stock < 0:
            raise ValueError(f"Cannot remove {quantity}mL. Current stock is only {self.current_stock}mL")
        
        return self.update_stock(new_stock, transaction_type)
    
    def reserve_stock(self, quantity):
        """Reserve stock for specific purposes"""
        if quantity > (self.current_stock - self.reserved_stock):
            raise ValueError(f"Cannot reserve {quantity}mL. Available stock is {self.current_stock - self.reserved_stock}mL")
        
        self.reserved_stock += quantity
        self.last_updated = datetime.utcnow()
        db.session.commit()
        return self
    
    def release_reserved_stock(self, quantity):
        """Release reserved stock"""
        if quantity > self.reserved_stock:
            raise ValueError(f"Cannot release {quantity}mL. Reserved stock is only {self.reserved_stock}mL")
        
        self.reserved_stock -= quantity
        self.last_updated = datetime.utcnow()
        db.session.commit()
        return self
    
    def update_expired_stock(self, expired_quantity):
        """Update expired stock count"""
        self.expired_stock = expired_quantity
        self.last_updated = datetime.utcnow()
        db.session.commit()
        return self
    
    def dispose_expired_stock(self):
        """Remove expired stock from inventory"""
        if self.expired_stock > 0:
            self.current_stock -= self.expired_stock
            disposed_quantity = self.expired_stock
            self.expired_stock = 0
            self.last_updated = datetime.utcnow()
            db.session.commit()
            return disposed_quantity
        return 0
    
    def reset_daily_counters(self):
        """Reset daily counters (typically called at midnight)"""
        self.units_dispensed_today = 0
        self.units_received_today = 0
        self.last_updated = datetime.utcnow()
        db.session.commit()
    
    def get_available_stock(self):
        """Get available stock (current - reserved - expired)"""
        return self.current_stock - self.reserved_stock - self.expired_stock
    
    def is_low_stock(self):
        """Check if stock is below minimum threshold"""
        return self.current_stock <= self.min_threshold
    
    def is_critical_stock(self):
        """Check if stock is critically low"""
        return self.current_stock <= (self.min_threshold * 0.5)
    
    def get_stock_status(self):
        """Get stock status description"""
        if self.is_critical_stock():
            return 'critical'
        elif self.is_low_stock():
            return 'low'
        elif self.current_stock >= self.max_capacity * 0.9:
            return 'high'
        else:
            return 'normal'
    
    def to_dict(self):
        """Convert inventory to dictionary"""
        return {
            'id': self.id,
            'blood_type': self.blood_type,
            'current_stock': float(self.current_stock),
            'min_threshold': float(self.min_threshold),
            'max_capacity': float(self.max_capacity),
            'reserved_stock': float(self.reserved_stock),
            'expired_stock': float(self.expired_stock),
            'available_stock': float(self.get_available_stock()),
            'units_dispensed_today': float(self.units_dispensed_today),
            'units_received_today': float(self.units_received_today),
            'is_low_stock': self.is_low_stock(),
            'is_critical_stock': self.is_critical_stock(),
            'stock_status': self.get_stock_status(),
            'last_updated': self.last_updated.isoformat(),
            'last_donation_date': self.last_donation_date.isoformat() if self.last_donation_date else None,
            'last_dispensed_date': self.last_dispensed_date.isoformat() if self.last_dispensed_date else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<BloodInventory {self.blood_type}: {self.current_stock}mL>'

# Marshmallow Schema for serialization
class BloodInventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BloodInventory
        load_instance = True

# Schema instances
inventory_schema = BloodInventorySchema()
inventories_schema = BloodInventorySchema(many=True) 