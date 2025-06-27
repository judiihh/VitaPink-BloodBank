from app import db, ma
from datetime import datetime, time

class Location(db.Model):
    """Location model for donation centers and blood banks"""
    __tablename__ = 'locations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Decimal(10, 8))
    longitude = db.Column(db.Decimal(11, 8))
    
    # Contact Information
    contact_info = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(255))
    website = db.Column(db.String(255))
    
    # Operating Hours
    opening_hours = db.Column(db.Text)  # JSON string with daily hours
    monday_open = db.Column(db.Time)
    monday_close = db.Column(db.Time)
    tuesday_open = db.Column(db.Time)
    tuesday_close = db.Column(db.Time)
    wednesday_open = db.Column(db.Time)
    wednesday_close = db.Column(db.Time)
    thursday_open = db.Column(db.Time)
    thursday_close = db.Column(db.Time)
    friday_open = db.Column(db.Time)
    friday_close = db.Column(db.Time)
    saturday_open = db.Column(db.Time)
    saturday_close = db.Column(db.Time)
    sunday_open = db.Column(db.Time)
    sunday_close = db.Column(db.Time)
    
    # Additional Information
    location_type = db.Column(db.String(50))  # 'blood_bank', 'hospital', 'mobile_unit', 'community_center'
    capacity = db.Column(db.Integer)  # Number of donors can be accommodated simultaneously
    amenities = db.Column(db.Text)  # Parking, accessibility, etc.
    languages_spoken = db.Column(db.String(255))  # Comma-separated languages
    
    # Status and Availability
    is_active = db.Column(db.Boolean, default=True)
    is_accepting_donations = db.Column(db.Boolean, default=True)
    current_wait_time = db.Column(db.Integer, default=0)  # Estimated wait time in minutes
    appointments_required = db.Column(db.Boolean, default=False)
    
    # Statistics
    total_donations_collected = db.Column(db.Integer, default=0)
    rating = db.Column(db.Decimal(3, 2))  # Average rating out of 5.00
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    donations = db.relationship('Donation', backref='location', lazy=True)
    
    def __init__(self, name, address, **kwargs):
        """Initialize location"""
        self.name = name
        self.address = address
        
        # Set additional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def add_location(cls, name, address, **kwargs):
        """Add a new donation location"""
        location = cls(name=name, address=address, **kwargs)
        db.session.add(location)
        db.session.commit()
        return location
    
    @classmethod
    def get_all_locations(cls, active_only=True):
        """Get all locations"""
        query = cls.query
        if active_only:
            query = query.filter_by(is_active=True)
        return query.all()
    
    @classmethod
    def get_location_by_id(cls, location_id):
        """Get location by ID"""
        return cls.query.get(location_id)
    
    @classmethod
    def get_locations_by_type(cls, location_type):
        """Get locations by type"""
        return cls.query.filter_by(location_type=location_type, is_active=True).all()
    
    @classmethod
    def get_locations_accepting_donations(cls):
        """Get all locations currently accepting donations"""
        return cls.query.filter_by(is_active=True, is_accepting_donations=True).all()
    
    @classmethod
    def search_locations_by_name(cls, search_term):
        """Search locations by name"""
        return cls.query.filter(
            cls.name.like(f'%{search_term}%'),
            cls.is_active == True
        ).all()
    
    def update_location(self, **kwargs):
        """Update location information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def deactivate_location(self):
        """Deactivate location"""
        self.is_active = False
        self.is_accepting_donations = False
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def activate_location(self):
        """Activate location"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update_wait_time(self, wait_time_minutes):
        """Update current wait time"""
        self.current_wait_time = wait_time_minutes
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def increment_donation_count(self):
        """Increment total donations collected"""
        self.total_donations_collected += 1
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def update_rating(self, new_rating):
        """Update location rating"""
        if 0 <= new_rating <= 5:
            self.rating = new_rating
            self.updated_at = datetime.utcnow()
            db.session.commit()
    
    def get_opening_hours_for_day(self, day_name):
        """Get opening hours for a specific day"""
        day_name = day_name.lower()
        if day_name == 'monday':
            return {'open': self.monday_open, 'close': self.monday_close}
        elif day_name == 'tuesday':
            return {'open': self.tuesday_open, 'close': self.tuesday_close}
        elif day_name == 'wednesday':
            return {'open': self.wednesday_open, 'close': self.wednesday_close}
        elif day_name == 'thursday':
            return {'open': self.thursday_open, 'close': self.thursday_close}
        elif day_name == 'friday':
            return {'open': self.friday_open, 'close': self.friday_close}
        elif day_name == 'saturday':
            return {'open': self.saturday_open, 'close': self.saturday_close}
        elif day_name == 'sunday':
            return {'open': self.sunday_open, 'close': self.sunday_close}
        return None
    
    def is_open_now(self):
        """Check if location is currently open"""
        now = datetime.now()
        day_name = now.strftime('%A').lower()
        current_time = now.time()
        
        hours = self.get_opening_hours_for_day(day_name)
        if hours and hours['open'] and hours['close']:
            return hours['open'] <= current_time <= hours['close']
        return False
    
    def get_languages_list(self):
        """Get list of languages spoken"""
        if self.languages_spoken:
            return [lang.strip() for lang in self.languages_spoken.split(',')]
        return []
    
    def calculate_distance(self, user_lat, user_lng):
        """Calculate approximate distance from user location (simplified)"""
        if not self.latitude or not self.longitude:
            return None
        
        # Simplified distance calculation (should use proper geolocation library)
        lat_diff = abs(float(self.latitude) - user_lat)
        lng_diff = abs(float(self.longitude) - user_lng)
        # Rough approximation: 1 degree ≈ 111 km
        distance_km = ((lat_diff ** 2 + lng_diff ** 2) ** 0.5) * 111
        return round(distance_km, 2)
    
    def to_dict(self, include_stats=False):
        """Convert location to dictionary"""
        location_dict = {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': float(self.latitude) if self.latitude else None,
            'longitude': float(self.longitude) if self.longitude else None,
            'contact_info': self.contact_info,
            'phone_number': self.phone_number,
            'email': self.email,
            'website': self.website,
            'location_type': self.location_type,
            'capacity': self.capacity,
            'amenities': self.amenities,
            'languages_spoken': self.get_languages_list(),
            'is_active': self.is_active,
            'is_accepting_donations': self.is_accepting_donations,
            'current_wait_time': self.current_wait_time,
            'appointments_required': self.appointments_required,
            'is_open_now': self.is_open_now(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'operating_hours': {
                'monday': {'open': self.monday_open.strftime('%H:%M') if self.monday_open else None,
                          'close': self.monday_close.strftime('%H:%M') if self.monday_close else None},
                'tuesday': {'open': self.tuesday_open.strftime('%H:%M') if self.tuesday_open else None,
                           'close': self.tuesday_close.strftime('%H:%M') if self.tuesday_close else None},
                'wednesday': {'open': self.wednesday_open.strftime('%H:%M') if self.wednesday_open else None,
                             'close': self.wednesday_close.strftime('%H:%M') if self.wednesday_close else None},
                'thursday': {'open': self.thursday_open.strftime('%H:%M') if self.thursday_open else None,
                            'close': self.thursday_close.strftime('%H:%M') if self.thursday_close else None},
                'friday': {'open': self.friday_open.strftime('%H:%M') if self.friday_open else None,
                          'close': self.friday_close.strftime('%H:%M') if self.friday_close else None},
                'saturday': {'open': self.saturday_open.strftime('%H:%M') if self.saturday_open else None,
                            'close': self.saturday_close.strftime('%H:%M') if self.saturday_close else None},
                'sunday': {'open': self.sunday_open.strftime('%H:%M') if self.sunday_open else None,
                          'close': self.sunday_close.strftime('%H:%M') if self.sunday_close else None}
            }
        }
        
        if include_stats:
            location_dict.update({
                'total_donations_collected': self.total_donations_collected,
                'rating': float(self.rating) if self.rating else None
            })
        
        return location_dict
    
    def __repr__(self):
        return f'<Location {self.name}>'

# Marshmallow Schema for serialization
class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Location
        load_instance = True
        include_relationships = True

# Schema instances
location_schema = LocationSchema()
locations_schema = LocationSchema(many=True) 