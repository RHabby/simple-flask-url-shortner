from flask import Blueprint


blueprint = Blueprint("test", __name__)


@blueprint.route("/")
def start_test():
    return "<h1>Hello there, morons!!</h1>"
