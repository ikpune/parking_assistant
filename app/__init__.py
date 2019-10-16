from flasgger import Swagger
import os
import logging
import sys
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# current config
config_name = os.environ.get("{}_env".format('test'), 'development')
current_config = config[config_name]

# Flask extensions
mail = Mail()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
swag = Swagger()

log_formatter = logging.Formatter((
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
))


def create_app(main=True):
    app = Flask(__name__)

    app.config['SWAGGER'] = {
        "swagger_version": "1.0",
        "title": "Parking Assistant API",
        "uiversion": 3,
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
            ('Access-Control-Allow-Credentials', "true"),
        ],
        "specs": [
            {
                "version": "0.0.1",
                "title": "API v1",
                "endpoint": 'v1_spec',
                "description": 'This is the version 1 of Parking Assistant API',
                "route": '/api/v1/spec'
            }
        ]
    }

    # swagger = Swagger(app)
    swag.init_app(app)

    CORS(app, supports_credentials=True)
    app.config.from_object(current_config)
    # app.json_encoder = CustomFlaskJSONEncoder
    mail.init_app(app)

    # Setup Flask-SQLAlchemy
    db.init_app(app)

    # Setup Flask-Marshmallow
    ma.init_app(app)

    # Setup Flask-Migrate
    migrate.init_app(app, db)

    # Setup Flask-User to handle user account related forms
    from .models.app_models import User

    # Import models so that they are registered with app
    from . import models  # noqa

    # Register web application routes
    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register API routes
    from app.api.v1 import api_v1 as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from app.api.v1.auth.urls import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1')

    from app.api.v1.parking_slots.urls import apps as apps_blueprint
    app.register_blueprint(apps_blueprint, url_prefix='/api/v1')

    from app.api.v1.users.urls import users as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/api/v1')

    # logger config
    package_name = '.'.join(__name__.split('.')[:-1])
    root_logger = logging.getLogger(package_name)

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    app.logger.addHandler(console_handler)
    console_handler.setFormatter(log_formatter)
    app.logger.setLevel(current_config.LOG_LEVEL)
    app.logger.info("server environment : {}".format(config_name))

    return app
