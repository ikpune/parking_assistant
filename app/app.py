import logging

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from flask import Blueprint


logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)


@main.before_app_request
def before_request():
    pass


@main.app_errorhandler(Exception)
def app_errorhandler(e):
    logger.debug('exception occured. Logging...')
    logger.exception(e)
