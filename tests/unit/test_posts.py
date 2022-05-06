from app.models import Song, Post
from app import create_app

app = create_app("config.TestingConfig")
app.app_context().push()

def test_post_model(test_db, persisted_song, persisted_user):
    new_post = Post(song_id=persisted_song.id, user_id=persisted_user.id, description="test post description")
    test_db.session.add(new_post)
    test_db.session.commit()

    assert new_post.id
    assert new_post.timestamp
    assert new_post.user == persisted_user