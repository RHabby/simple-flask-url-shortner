from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

from app.url_shortener.models import Link


def create_app(config="config.py"):
    flask_app = Flask(__name__)
    flask_app.config.from_pyfile(config)

    db.init_app(flask_app)
    migrate.init_app(app=flask_app, db=db)

    from app.views import blueprint as test
    flask_app.register_blueprint(blueprint=test)

    from app.url_shortener.views import blueprint as url_shortener
    flask_app.register_blueprint(blueprint=url_shortener)

    return flask_app
