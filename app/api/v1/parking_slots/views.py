import logging
import traceback
from flask import jsonify, g, request, Response, json
from flask.views import MethodView

from werkzeug.exceptions import NotFound
from sqlalchemy.exc import DatabaseError, IntegrityError
from marshmallow.exceptions import ValidationError

from app import db
from app.decorators import auth
from app.models.app_models import ParkingSlots, UserParkingSlots
from ..helpers.helper import RequestHelper

from config.common import Config

from .serializers import ParkingSlotsSchema
from .helper import UserParkingSlotsHelper


logger = logging.getLogger(__name__)


class UserParkingSlotsAPI(MethodView):

    @auth.login_required
    def get(self):
        """
            GET List of User's Parking Slots
            ---
                responses:
                    200:
                        description: Returns list of parking_slots assigned to user.
                    400:
                        description: Any DB error occurred.
                    401:
                        description: Only valid users can access.
        """
        try:

            user_parking_slots_helper = UserParkingSlotsHelper()
            response_data = user_parking_slots_helper.get_user_parking_slots_data()

        except DatabaseError as de:
            logger.error("User Parking Slots List: Error while populating parking slots list. " + str(de))
            return jsonify(err_msg="Error while populating parking slot list!"), 400

        except Exception as e:
            logger.error("User Parking Slot List: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while populating Parking Slot list!"), 400

        return Response(json.dumps(response_data),
                        status=200,
                        mimetype='application/json')

    @auth.login_required
    def post(self):
        """
            POST Creates a new parking slot reservation.
            ---
                parameters:
                  - name: parking_slot_id
                    in: body
                    type: string
                    required: true
                responses:
                    201:
                        description: Returns parking slot data.
                    400:
                        description: Parking slot with entered user already exists or DB error occurred.
        """
        data = RequestHelper.get_request_data(request)

        parking_slot_id = data.get('parking_slot_id', None)

        if not parking_slot_id:
            return jsonify(err_msg="Parking SLot id not provided!"), 400

        parking_slot = ParkingSlots.query.filter(ParkingSlots.id == parking_slot_id).first()

        try:
            if parking_slot:
                return jsonify(err_msg="Parking Slot with parking_slot_id already exists!"), 400

            else:
                parking_slot_schema = ParkingSlotsSchema()
                parking_slot = ParkingSlots(name=parking_slot_id)
                db.session.add(parking_slot)
                db.session.commit()

                parking_slot_data = parking_slot_schema.dump(ParkingSlots.query.get(parking_slot.id))

        except IntegrityError as ie:
            logger.error("Parking Slot Create: Error while creating parking slot. " + str(ie))
            return jsonify(err_msg="Error while creating parking slot. "
                                   "parking slot with parking_slot_id already exists!"), 400

        except DatabaseError as de:
            logger.error("parking slot List: Error while populating parking slot list. " + str(de))
            return jsonify(err_msg="Error while populating parking slot list!"), 400

        except Exception as e:
            logger.error("parking slot List: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while populating parking slot list!"), 400

        return Response(json.dumps(parking_slot_data),
                        status=200,
                        mimetype='application/json')

    @auth.login_required
    def put(self):
        """
            PUT makes the reservation for parking slot
            ---
                parameters:
                  - name: parking_slot
                    in: body
                    type: string
                    required: true
                    example: "1"
                responses:
                    201:
                        description: Parking Slot details updated successfully.
                    400:
                        description: User doesn't exists or any DB error occurred.
                    422:
                        description: Request parameters validation errors.
        """
        data = RequestHelper.get_request_data(request)

        parking_slots_data = data.get('parking_slots', None)

        if not parking_slots_data:
            return jsonify(err_msg="Parking slots details are not provided!"), 400

        app_schema = ParkingSlotsSchema(many=True)

        try:
            data = app_schema.load(parking_slots_data)

        except ValidationError as ve:
            return jsonify(err_msg=ve.messages), 422

        try:

            for parking_slots in data:
                user_parking_slot = UserParkingSlots.query.get_or_404(parking_slot_id=int(parking_slots.get('id')))
                parking_slot = ParkingSlots.query.get_or_404(int(parking_slots.get('id')))

                if user_parking_slot:
                    user_parking_slot.user_id = g.current_user.id
                    parking_slot.is_resevec = False
                    db.session.add(user_parking_slot)
                    db.session.add(parking_slot)
                    db.session.commit()

            logger.info("Update parking slot: parking slot details updated successfully.")

        except NotFound as ne:
            logger.error("Users List: Error while fetching user record. " + str(ne))
            return jsonify(err_msg="User doesn't exists!"), 404

        except DatabaseError as de:
            logger.error("Update parking slot: Error while updating parking slot. " + str(de))
            return jsonify(err_msg="Error while updating parking slot!"), 400

        except Exception as e:
            logger.error("Update parking slot: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while updating parking slot details!"), 400

        return Response(status=201, mimetype='application/json')


class ParkingSlotsAPI(MethodView):

    @auth.login_required
    def get(self):
        """
            GET List of all the available Parking Slots
            ---
                parameters:
                  - name: is_reserved
                    in: path
                    type: integer
                    required: false
                    description: If passed as a request parameter and with value 1,
                                list of free parking_slots will be returned. Otherwise list of all parking_slots.
                                E.g. '/api/v1/parking_slots/settings?is_reserved=1'
                responses:
                    200:
                        description: Returns list of all available parking_slots.
                    400:
                        description: Any DB error occurred or Value error occurred.
        """
        parking_slots_schema = ParkingSlotsSchema(many=True)

        get_free_parking_slots = request.args.get('is_reserved', None)

        try:

            if not get_free_parking_slots:
                try:
                    get_free_parking_slots = bool(int(get_free_parking_slots))

                except ValueError as ve:
                    logger.error("Parking Slots List: Error while populating parking slots list. " + str(ve))
                    return jsonify(err_msg="Please check the value for request parameter 'is_reserved'! "
                                           "It should be either 1 or 0"), 400

            if get_free_parking_slots:
                parking_slots = ParkingSlots.query.filter(not ParkingSlots.is_reserved)

            result = parking_slots_schema.dump(parking_slots)
            logger.info("Parking Slots List:Parking Slots List populated successfully.")

        except DatabaseError as de:
            logger.error("Parking Slots List: Error while populating Parking Slots list. " + str(de))
            return jsonify(err_msg="Error while populating Parking Slots list!"), 400

        except Exception as e:
            logger.error("Parking Slots List: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while populating Parking Slots list!"), 400

        return Response(json.dumps(result),
                        status=200,
                        mimetype='application/json')
