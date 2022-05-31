from app import db
import os
from os import path
from app.models import User
from app import create_app
from dotenv import load_dotenv

basedir = os.path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))
app = create_app()

db.drop_all()
db.create_all()

User.signup(
    username="pixls",
    password="Q^T)n!nFd^q-sxNw.@gt",
    email="yara@beadenkopf.com",
    avatar=None,
    bio="it's me pixls",
    admin=True
)

db.session.commit()
