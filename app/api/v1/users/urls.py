from flask import Blueprint, jsonify
from flask_cors import CORS

from app.api.v1.users.views import UserAPI

users = Blueprint('user', __name__)

CORS(users)

user_view = UserAPI.as_view('user_view')
users.add_url_rule('/users/', view_func=user_view, methods=['GET', 'POST', ])
users.add_url_rule('/users/<int:user_id>/', view_func=user_view,
                   methods=['GET', 'PUT', 'DELETE', ], strict_slashes=False)


@users.app_errorhandler(404)
def page_not_found(e):
    return jsonify(err_msg="Requested URL not found on this server!"), 404


@users.app_errorhandler(405)
def page_not_found(e):
    return jsonify(err_msg="The method is not allowed for the requested URL!"), 405


@users.app_errorhandler(500)
def page_not_found(e):
    return jsonify(err_msg="Internal server error!"), 500
