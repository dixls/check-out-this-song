import os
from os import environ, path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

basedir = os.path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_type="config.DevelopmentConfig"):

    app = Flask(__name__)

    if os.getenv("CONFIG_TYPE"):
        CONFIG_TYPE = os.getenv("CONFIG_TYPE")
        app.config.from_object(CONFIG_TYPE)
    else:
        app.config.from_object(config_type)

    db.app = app
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import views
        db.create_all()
        app.register_blueprint(views.main)

        return app
