import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(basedir, "..", ".env"))


SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, '..', 'app.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY")
