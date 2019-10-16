import os

from .common import Config


class DevelopmentConfig(Config):
    DEBUG = True
    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')
    LOG_FILE_LOCATION = '{}/{}'.format(os.getcwd(), 'temp/app.log')
