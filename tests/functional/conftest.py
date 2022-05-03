from app import create_app
import pytest
from app import db


@pytest.fixture
def test_app():
    app = create_app("config.TestingConfig")
    app.config.from_object("config.TestingConfig")
    return app


@pytest.fixture
def test_db(test_app):
    db.create_all()
    yield db
    db.session.close()
    db.drop_all()
