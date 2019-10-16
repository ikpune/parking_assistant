from functools import wraps

from flask import current_app, g
from flask import request, Response, jsonify
import logging

from ..api.v1.helpers.helper import AuthUserHelper
from app.models.app_models import User
from werkzeug.security import check_password_hash

logger = logging.getLogger(__name__)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """

    try:
        import pdb; pdb.set_trace()
        user = User.query.filter(User.username == str(username)).first()

        if user and check_password_hash(user.password, password):
            g.current_user = user
            return True
        else:
            return False

    except Exception as e:
        logger.error("Auth: Error while fetching user data!")

    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return jsonify(status=False, msg='Could not verify your access level for this URL. '
                                     'You have to login with proper credentials'), 401, \
           {'WWW-Authenticate': 'Basic realm="Login Required"'}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.debug("in auth decorator")
        if current_app.config['IS_AUTH_ENABLED']:
            logger.debug("AUTH is ENABLED")
            auth = request.authorization
            if not auth or not AuthUserHelper.check_for_auth(auth.username, auth.password):
                return authenticate()
            return f(*args, **kwargs)
        else:
            logger.debug("AUTH is DISABLED")
    return decorated
