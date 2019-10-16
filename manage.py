#!/usr/bin/python
from flask.cli import FlaskGroup
from app import create_app

from flask_script import Manager
from app.commands import CreateUsersCommand, CreateParkignSlotsCommand

cli = FlaskGroup(create_app=create_app)

# Setup Flask-Script with command line commands
manager = Manager(create_app)
manager.add_command('create_users', CreateUsersCommand)
manager.add_command('create_parking_slots', CreateParkignSlotsCommand)

if __name__ == '__main__':
    manager.run()
    cli()
