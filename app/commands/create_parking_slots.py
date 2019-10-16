"""Command classes for create dummy parking slots command"""

from flask_script import Command
from sqlalchemy import exc

from app import db
from app.models.app_models import ParkingSlots


class CreateParkignSlotsCommand(Command):

    def run(self):
        create_parking_slots()
        print('Parking slots are created.')


def create_parking_slots():
    """ Create parking slots """

    # Create all tables
    db.create_all()

    # Add lat long values for parking slots
    find_or_create_parking_slot(35.929673, -78.948237)
    find_or_create_parking_slot(38.889510, -77.032000)
    find_or_create_parking_slot(38.032120, -78.477510)
    find_or_create_parking_slot(36.379450, -75.830290)

    # Save to DB
    db.session.commit()


def find_or_create_parking_slot(plat, plong):
    """ Find existing user or create new user """
    parking_slot = ParkingSlots.query.filter(ParkingSlots.lat == plat).first()

    try:
        if not parking_slot:
            parking_slot = ParkingSlots(lat=plat, long=plong)

            db.session.add(parking_slot)
    except exc.IntegrityError as e:
        print("Exception occurred while creating parking slot : " + e)
