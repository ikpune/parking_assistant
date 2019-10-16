import logging
import traceback
from flask import jsonify, request, g, Response, json
from flask.views import MethodView

from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import NotFound

from app.api.v1.users.serializers import UserSchema
from app.api.v1.helpers.helper import AuthUserHelper
from app.api.v1.parking_slots.helper import UserParkingSlotsHelper

logger = logging.getLogger(__name__)


class LoginAPI(MethodView):

    def get(self):
        print("in auth login")
        """
             Check for user credentials
             ---
                responses:
                    200:
                        description: Returns user object with assigned parking_slots.
                    401:
                        description: For invalid credentials.
        """
        auth = request.authorization

        if not auth:
            return jsonify(err_msg="No authorization details are present in the header!"), 400

        try:
            if AuthUserHelper.check_for_auth(auth.username, auth.password):
                logger.info("Login: Login Successful!")

                user_schema = UserSchema()
                result = user_schema.dump(g.current_user)

                user_parking_slots_helper = UserParkingSlotsHelper()
                result['user']['parking_slots'] = user_parking_slots_helper.get_user_parking_slots_data()

                return Response(json.dumps(result),
                                status=200,
                                mimetype='application/json')

            else:
                return jsonify(err_msg="Login Failed! Invalid Credentials"), 401

        except DatabaseError as de:
            logger.error("Login: Error while logging in user. DB error. " + str(de))
            return jsonify(err_msg="Error while logging in user!"), 400

        except Exception as e:
            logger.error("Login: Error while fetching user data!\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Login Failed! Error in processing request."), 400
