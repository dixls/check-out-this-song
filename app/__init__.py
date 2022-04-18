import os
from flask import Flask
from .views import main
from .extensions import db


def create_app():

    app = Flask(__name__)

    CONFIG_TYPE = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(CONFIG_TYPE)

    db.init_app(app)

    app.register_blueprint(main)

    return app
