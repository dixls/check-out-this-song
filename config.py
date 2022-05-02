import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base configuration class. Contains default config settings.
    """

    SQLALCHEMY_DATABASE_URI = "postgresql:///cots"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    FLASK_ENV = "development"
    WTF_CSRF_ENABLED = True
    SECRET_KEY = os.getenv("SECRET_KEY", default="DEFAULT SECRET KEY")
    LASTFM_KEY = os.getenv("LASTFM_KEY", default="")
    LASTFM_SECRET = os.getenv("LASTFM_SECRET", default="")
    YOUTUBE_KEY = os.getenv("YOUTUBE_KEY", default="")
    BCRYPT_LOG_ROUNDS = 14
    BCRYPT_HANDLE_LONG_PASSWORDS = True


class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY", default="DEV SECRET KEY")
    TESTING = False
    DEBUG = True


class TestingConfig(Config):
    WTF_CSRF_ENABLED = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_ENABLED = False
    SECRET_KEY = "TEST SECRET KEY"


class ProductionConfig(Config):
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URL", default="postgresql:///cots"
    )
