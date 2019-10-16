import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    DEBUG = False
    TESTING = False
    IS_AUTH_ENABLED = True
    IS_ERROR_MAIL_ENABLED = False

    LOG_LEVEL = logging.DEBUG

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '51f52814-0071-11e6-a247-000ec6c2372c')
    REQUEST_STATS_WINDOW = 15

    MEDIA_DIR = '/media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
    TEMP_DIR = '{}/{}'.format(BASE_DIR, 'temp')

    LOG_FILE_LOCATION = '/var/log/test.log'

    CONTENT_ISSUES_EMAIL_IDS = []

    SERVER_URL = 'localhost'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../parkingassistant.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids a SQLAlchemy Warning