from flask_user import UserMixin
from app import db
from datetime import datetime


# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    phone = db.Column(db.Unicode(15), nullable=False, server_default=u'', unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    parking_slots = db.relationship('ParkingSlots', secondary='user_parking_slots')


class ParkingSlots(db.Model):
    __tablename__ = 'parking_slots'

    id = db.Column(db.Integer(), primary_key=True)
    lat = db.Column(db.Float(), nullable=False, unique=True)
    long = db.Column(db.Float(), nullable=False, unique=True)
    is_reserved = db.Column(db.Boolean(), nullable=False, server_default='0')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    users = db.relationship('User', secondary='user_parking_slots')


class UserParkingSlots(db.Model):
    __tablename__ = 'user_parking_slots'

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    parking_slot_id = db.Column(db.Integer(), db.ForeignKey('parking_slots.id', ondelete='CASCADE'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship(User, backref=db.backref("user_parking_slots", cascade="all, delete-orphan"))
    parking_slot = db.relationship(ParkingSlots, backref=db.backref("user_parking_slots", cascade="all, delete-orphan"))

    def __init__(self, parking_slot=None, user=None):
        self.user = user
        self.parking_slot = parking_slot
