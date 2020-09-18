from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config="config.py"):
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile(config)

    csrf.init_app(flask_app)
    db.init_app(flask_app)
    migrate.init_app(app=flask_app, db=db)

    from app.url_shortener.views import blueprint as url_shortener
    flask_app.register_blueprint(blueprint=url_shortener)
    # register_bps(flask_app)

    return flask_app


def register_bps(flask_app):
    from app.url_shortener.views import blueprint as url_shortener
    flask_app.register_blueprint(blueprint=url_shortener)
