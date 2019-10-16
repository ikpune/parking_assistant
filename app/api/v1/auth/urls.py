from flask import Blueprint, jsonify
from flask_cors import CORS

from .views import LoginAPI

auth = Blueprint('auth', __name__)

CORS(auth)

login_view = LoginAPI.as_view('login_api')
auth.add_url_rule('/login/', view_func=login_view, methods=['GET', ])


@auth.app_errorhandler(404)
def page_not_found(e):
    return jsonify(err_msg="Requested URL not found on this server!"), 404


@auth.app_errorhandler(405)
def page_not_found(e):
    return jsonify(err_msg="The method is not allowed for the requested URL!"), 405


@auth.app_errorhandler(500)
def page_not_found(e):
    return jsonify(err_msg="Internal server error!"), 500