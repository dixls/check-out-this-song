from app import create_app
from app.models import User

app = create_app("config.TestingConfig")
app.app_context().push()


def test_user_model(new_user, test_db):
    """just a test test"""
    test_db.session.add(new_user)
    test_db.session.commit()

    assert new_user.id


def test_user_authenticate(persisted_user, test_db):
    """
    Testing whether authentication given the correct credentials returns the user object
    """
    user = User.authenticate(persisted_user.username, "unhashed-pw")

    assert user.username == persisted_user.username


def test_user_authenticate_fail(persisted_user, test_db):
    """
    Testing whether given bad password for an existing username, authentication fails
    """
    user = User.authenticate(persisted_user.username, "wrong password")

    assert user == False


def test_user_authenticate_no_user(test_db):
    """
    Testing whether given a username that does not exist authentication fails
    """
    user = User.authenticate("not_user", "unhashed-pw")

    assert user == False