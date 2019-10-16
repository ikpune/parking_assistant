"""Command classes for create dummy users command"""

import datetime

from flask import current_app
from flask_script import Command

from app import db
from app.models.app_models import User

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc


class CreateUsersCommand(Command):

    def run(self):
        create_users()
        print('Users are created.')


def create_users():
    """ Create users """

    # Create all tables
    db.create_all()

    # Add users
    find_or_create_user(u'user1', u'Test', u'User 1', 'Password1', 1234567890)
    find_or_create_user(u'user1', u'Test', u'User 2', 'Password1', 1234567891)

    # Save to DB
    db.session.commit()


def find_or_create_user(first_name, last_name, username, password, phone):
    """ Find existing user or create new user """
    user = User.query.filter(User.username == username).first()

    try:
        if not user:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        password=generate_password_hash(password),
                        phone=phone,
                        active=True
                        )

            db.session.add(user)

    except exc.IntegrityError as e:
        print("Exception occured while creating users : " + e)
