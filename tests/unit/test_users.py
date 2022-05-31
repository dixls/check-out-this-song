from cgi import test
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


def test_follows(test_db, persisted_user, persisted_2nd_user):
    """
    Test whether the following relationship works as expected
    """
    persisted_user.following.append(persisted_2nd_user)
    test_db.session.commit()

    assert persisted_2nd_user in persisted_user.following
    assert persisted_user in persisted_2nd_user.followers
    assert persisted_2nd_user not in persisted_user.followers
    assert persisted_user not in persisted_2nd_user.following


def test_unfollow(test_db, persisted_user_with_follow, persisted_2nd_user):

    persisted_user_with_follow.following.remove(persisted_2nd_user)
    test_db.session.commit()

    assert persisted_2nd_user not in persisted_user_with_follow.following
    assert persisted_user_with_follow not in persisted_2nd_user.followers
    assert persisted_2nd_user not in persisted_user_with_follow.followers
    assert persisted_user_with_follow not in persisted_2nd_user.following


def test_like(test_db, persisted_user, persisted_2nd_user, persisted_post):

    persisted_user.liked_posts.append(persisted_post)
    test_db.session.commit()

    assert persisted_post in persisted_user.liked_posts
    assert persisted_post not in persisted_2nd_user.liked_posts
    

def test_unlike(test_db, persisted_user_with_likes, persisted_2nd_user, persisted_post):

    persisted_user_with_likes.liked_posts.remove(persisted_post)
    test_db.session.commit()

    assert persisted_post not in persisted_user_with_likes.liked_posts
    assert persisted_post not in persisted_2nd_user.liked_posts
    