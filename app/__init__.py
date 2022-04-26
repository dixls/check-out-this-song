import os
from dotenv import load_dotenv
from flask import Flask
from .views import main
from .extensions import db, login_manager

load_dotenv()

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

    app.register_blueprint(main)

    return app
