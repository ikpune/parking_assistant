import logging
import os

from .common import Config


class ProductionConfig(Config):
    DEBUG = True
    MEDIA_DIR = 'media'
    FILES_DIR = '{}/{}'.format(MEDIA_DIR, 'files')

    LOG_LEVEL = logging.INFO
