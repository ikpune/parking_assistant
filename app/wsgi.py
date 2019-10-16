import os

from app import create_app

# Create an application instance that web servers can use. We store it as
# "application" (the uwsgi default) and also the much shorter and convenient
# "app".

application = app = create_app()

if __name__ == '__main__':
    application().run()

