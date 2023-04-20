import os
from flask import Flask
from flask import url_for
from application.config import LocalDevelopmentConfig
from application.data.models import db
#from application.utils.security import login_manager
from application.jobs.workers import celery_init_app
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache
from flask_mail import Mail

app = None
redis_cache = None

# creating and binding of our flask application
def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    redis_cache = Cache(app)
    CORS(app)
    mail = Mail(app)
    bcrypt = Bcrypt(app)
#    sec.init_app(app, user_datastore)
    login_manager = LoginManager(app)
#    login_manager.init_app(app)
    app.app_context().push()

    app.config.from_mapping(
        CELERY = dict(
            broker_url = app.config['CELERY_BROKER_URL'],
            result_backend = app.config['CELERY_RESULT_BACKEND'],
            timezone = "Asia/Calcutta",
            enable_utc = False
        ),
    ) 

    celery = celery_init_app(app)

    app.app_context().push()
    return app, redis_cache, celery, mail, bcrypt, login_manager


app, cache, celery, mail, bcrypt, login_manager = create_app()


from application.controller.controllers import *

from application.controller.api import *


if __name__ == '__main__':
  # Run the Flask app
  app.run()
