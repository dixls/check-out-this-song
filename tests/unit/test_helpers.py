from app.helpers import get_user

def test_get_user_should_succeed_with_true(app, test_db, persisted_user):
    results = get_user(persisted_user.username, persisted_user)

    assert results == (True, persisted_user)


def test_get_user_should_succeed_with_false(app,test_db, persisted_user, persisted_2nd_user):
    results = get_user(persisted_user.username, persisted_2nd_user)

    assert results == (False, persisted_user)


def test_get_user_should_fail(app,test_db, persisted_user):
    results = get_user("not_a_real_username", persisted_user)

    assert results == False
    
