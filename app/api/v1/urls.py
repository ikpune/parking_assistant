from flask import Blueprint, jsonify
from flask_cors import CORS

api_v1 = Blueprint('api.v1', __name__)

CORS(api_v1)


@api_v1.app_errorhandler(404)
def page_not_found(e):
    return jsonify(status=False, message="Requested URL not found on this server!"), 404


@api_v1.app_errorhandler(405)
def page_not_found(e):
    return jsonify(status=False, message="The method is not allowed for the requested URL!"), 405


@api_v1.app_errorhandler(500)
def page_not_found(e):
    return jsonify(status=False, message="Internal server error!"), 500
