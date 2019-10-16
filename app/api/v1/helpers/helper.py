import logging
from flask import g

from werkzeug.security import check_password_hash
from sqlalchemy.exc import DatabaseError

from app.models.app_models import User

logger = logging.getLogger(__name__)


class AuthUserHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def check_for_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """

        try:
            user = User.query.filter(User.username == str(username)).first()

            if user and check_password_hash(user.password, password):
                g.current_user = user
                return user

        except DatabaseError as e:
            logger.error("Auth: Error while fetching user data!")

        return False


class RequestHelper(object):

    def __init__(self):
        pass

    @staticmethod
    def get_request_data(request):
        if request.mimetype == 'application/json':
            data = request.get_json()
        else:
            data = request.form.to_dict()

        return data
