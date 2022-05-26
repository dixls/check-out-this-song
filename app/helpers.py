from app.models import User
from sqlalchemy import exc
from flask import abort

def get_user(username, current_user):
    try:
            user = User.query.filter_by(username=username).one()
    except exc.SQLAlchemyError:
        return False
    match = False
    if current_user == user:
        match = True
    return (match, user)