from flask import Blueprint, jsonify
from flask_cors import CORS

from .views import UserParkingSlotsAPI, ParkingSlotsAPI

apps = Blueprint('parking_slots', __name__)

CORS(apps)

userparkingslots_view = UserParkingSlotsAPI.as_view('userparkingslot_api')
apps.add_url_rule('/parking_slots/userparkingslots/', view_func=userparkingslots_view, methods=['GET', 'POST', 'PUT', ]
                  , strict_slashes=False)

parkingslots_view = ParkingSlotsAPI.as_view('parkingslots_api')
apps.add_url_rule('/parking_slots/settings/', view_func=parkingslots_view, methods=['GET', ], strict_slashes=False)


@apps.app_errorhandler(404)
def page_not_found(e):
    return jsonify(err_msg="Requested URL not found on this server!"), 404


@apps.app_errorhandler(405)
def page_not_found(e):
    return jsonify(err_msg="The method is not allowed for the requested URL!"), 405


@apps.app_errorhandler(500)
def page_not_found(e):
    return jsonify(err_msg="Internal server error!"), 500