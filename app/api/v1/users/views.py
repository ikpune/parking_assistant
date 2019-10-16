import logging
import traceback
from flask.views import MethodView
from flask import jsonify, request, Response, json

from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import DatabaseError, IntegrityError
from marshmallow import ValidationError

from app import db
from app.decorators import auth
from app.models.app_models import User, ParkingSlots, UserParkingSlots
from app.api.v1.users.serializers import UserSchema, UserModelSchema
from ..helpers.helper import (RequestHelper)

logger = logging.getLogger(__name__)


class UserAPI(MethodView):

    @auth.login_required
    def get(self, user_id=None):
        """
             GET List of All Users or details of a User.
             ---
                parameters:
                  - name: user_id
                    type: integer
                    in: path
                    required: false
                    description: ID of a user.
                responses:
                    200:
                        description: Returns list of all users or details of a user.
                    400:
                        description: Any DB error occurred.
                    401:
                        description: Only Admin Role Users can access.
        """

        try:
            user_schema = UserSchema()
            users_schema = UserModelSchema(many=True)

            if user_id:
                user = User.query.get_or_404(int(user_id))
                result = user_schema.dump(user)
            else:
                users = User.query.all()
                result = users_schema.dump(users)

            logger.info("Users List: Users List populated successfully.")

        except NotFound as ne:
            logger.error("Users List: Error while fetching user record. " + str(ne))
            return jsonify(err_msg="User doesn't exists!"), 404

        except Exception as e:
            logger.error("Users List: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while populating Users list!"), 400

        return Response(json.dumps(result),
                        status=200,
                        mimetype='application/json')

    @auth.login_required
    def post(self):
        """
            POST Creates a new user.
            ---
                parameters:
                  - name: user
                    in: body
                    type: object
                    required: true
                    example: {
                                "username":"test",
                                "password":"test",
                                "first_name":"test",
                                "last_name":"test",
                                "phone":"1234567890"
                            }
                definitions:
                    user:
                        type: object
                        properties:
                            username:
                                type: string
                            password:
                                type: string
                            first_name:
                                type: string
                            last_name:
                                type: string
                            phone:
                                type: string
                                description: user phone
                responses:
                    201:
                        description: Returns user's details.
                    400:
                        description: User with entered username already exists or DB error occurred.
                    422:
                        description: Request parameters validation errors.
        """
        data = RequestHelper.get_request_data(request)

        user_data = data.get('user', None)

        if not user_data:
            return jsonify(err_msg="User details are not provided!"), 400

        user_schema = UserSchema()

        try:
            data = user_schema.load(user_data)
        except ValidationError as ve:
            return jsonify(err_msg=ve.messages), 422

        # TODO: Handling user creation in helper functions
        try:

            user = User(
                username=data.get('username'),
                password=generate_password_hash(data.get('password')),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                is_active=True
            )


            db.session.add(user)
            db.session.commit()

            logger.info("Create User: New user created successfully.")
            result = user_schema.dump(User.query.get(user.id))

        except IntegrityError as ie:
            logger.error("User Create: Error while creating User. " + str(ie))
            return jsonify(err_msg="Error while creating user. "
                                   "User with this username already exists!"), 400

        except DatabaseError as de:
            logger.error("Create User: Error while creating user record. " + str(de))
            return jsonify(err_msg="Error while creating new user!"), 400

        except Exception as e:
            logger.error("Create User: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while creating new user!"), 400

        return Response(json.dumps(result),
                        status=201,
                        mimetype='application/json')

    @auth.login_required
    def delete(self, user_id):
        """
             DELETE Deletes a user with user_id.
             ---
                parameters:
                  - name: user_id
                    type: integer
                    in: path
                    required: true
                    description: ID of a user.
                responses:
                    200:
                        description: Deletes the user with user id.
                    400:
                        description: Any DB error occurred.
        """
        try:
            user = User.query.get_or_404(int(user_id))

            parking_slots = ParkingSlots.query.filter(id__in=user.parking_slots)
            for ps in parking_slots:
                ps.is_reserved = False
                db.session.add(ps)

            db.session.delete(user)
            db.session.commit()

            logger.info("Delete User: User deleted successfully.")

        except NotFound as ne:
            logger.error("Delete User: Error while deleting user record. " + str(ne))
            return jsonify(err_msg="User doesn't exists!"), 404

        except DatabaseError as de:
            logger.error("Delete User: Error while deleting user record. " + str(de))
            return jsonify(err_msg="Error while deleting user record!"), 400

        except Exception as e:
            logger.error("Delete User: Error while processing request.\n"
                         + str(e) + "\n" + str(traceback.print_exc()))
            return jsonify(err_msg="Error while updating user record!"), 400

        return Response(status=200)
