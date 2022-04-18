from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def root():
    return "Blueprint root"
