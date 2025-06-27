from app import db, ma
from datetime import datetime
from enum import Enum

class DonationStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Donation(db.Model):
    """Donation model for tracking blood donations"""
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)
    quantity = db.Column(db.Decimal(10, 2), nullable=False)  # in mL
    donation_date = db.Column(db.DateTime, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    status = db.Column(db.Enum(DonationStatus), default=DonationStatus.PENDING)
    
    # Additional donation information
    hemoglobin_level = db.Column(db.Decimal(4, 2))  # g/dL
    blood_pressure_systolic = db.Column(db.Integer)
    blood_pressure_diastolic = db.Column(db.Integer)
    weight = db.Column(db.Decimal(5, 2))  # kg
    temperature = db.Column(db.Decimal(4, 1))  # Celsius
    
    # Processing information
    collection_bag_number = db.Column(db.String(50))
    expiry_date = db.Column(db.DateTime)
    processing_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, blood_type, quantity, donation_date, location_id=None, **kwargs):
        """Initialize donation record"""
        self.user_id = user_id
        self.blood_type = blood_type
        self.quantity = quantity
        self.donation_date = donation_date
        self.location_id = location_id
        
        # Set additional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def record_donation(cls, user_id, blood_type, quantity, donation_date, location_id=None, **kwargs):
        """Record a new donation"""
        donation = cls(
            user_id=user_id,
            blood_type=blood_type,
            quantity=quantity,
            donation_date=donation_date,
            location_id=location_id,
            **kwargs
        )
        db.session.add(donation)
        db.session.commit()
        return donation
    
    @classmethod
    def get_donations_by_user(cls, user_id):
        """Get all donations for a specific user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.donation_date.desc()).all()
    
    @classmethod
    def get_all_donations(cls, status=None):
        """Get all donations, optionally filtered by status"""
        query = cls.query
        if status:
            query = query.filter_by(status=status)
        return query.order_by(cls.donation_date.desc()).all()
    
    @classmethod
    def get_donations_by_date_range(cls, start_date, end_date):
        """Get donations within a date range"""
        return cls.query.filter(
            cls.donation_date >= start_date,
            cls.donation_date <= end_date
        ).order_by(cls.donation_date.desc()).all()
    
    @classmethod
    def get_donations_by_blood_type(cls, blood_type):
        """Get donations by blood type"""
        return cls.query.filter_by(blood_type=blood_type).order_by(cls.donation_date.desc()).all()
    
    @classmethod
    def get_donations_by_location(cls, location_id):
        """Get donations by location"""
        return cls.query.filter_by(location_id=location_id).order_by(cls.donation_date.desc()).all()
    
    def update_donation_status(self, status, notes=None):
        """Update donation status"""
        self.status = status
        if notes:
            self.processing_notes = notes
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update_donation(self, **kwargs):
        """Update donation information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def complete_donation(self, collection_bag_number=None, expiry_date=None):
        """Mark donation as completed"""
        self.status = DonationStatus.COMPLETED
        if collection_bag_number:
            self.collection_bag_number = collection_bag_number
        if expiry_date:
            self.expiry_date = expiry_date
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel_donation(self, reason=None):
        """Cancel donation"""
        self.status = DonationStatus.CANCELLED
        if reason:
            self.processing_notes = reason
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert donation to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'blood_type': self.blood_type,
            'quantity': float(self.quantity),
            'donation_date': self.donation_date.isoformat(),
            'location_id': self.location_id,
            'status': self.status.value,
            'hemoglobin_level': float(self.hemoglobin_level) if self.hemoglobin_level else None,
            'blood_pressure_systolic': self.blood_pressure_systolic,
            'blood_pressure_diastolic': self.blood_pressure_diastolic,
            'weight': float(self.weight) if self.weight else None,
            'temperature': float(self.temperature) if self.temperature else None,
            'collection_bag_number': self.collection_bag_number,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'processing_notes': self.processing_notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Donation {self.id}: {self.blood_type} - {self.quantity}mL>'

# Marshmallow Schema for serialization
class DonationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Donation
        load_instance = True
        include_relationships = True

# Schema instances
donation_schema = DonationSchema()
donations_schema = DonationSchema(many=True) 