from hashlib import new
from app import create_app

app = create_app("config.TestingConfig")
app.app_context().push()


def test_user_model(new_user, test_db):
    """just a test test"""
    test_db.session.add(new_user)
    test_db.session.commit()

    assert new_user.id