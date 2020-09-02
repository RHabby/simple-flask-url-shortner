import string
from random import choices
from datetime import datetime

from app import db


class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_link = db.Column(db.String(256))
    short_link = db.Column(db.String(6), unique=True)
    creation_time = db.Column(db.DateTime, default=datetime.now)
    visits = db.Column(db.Integer, default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_link = self.generate_short_link()

    def generate_short_link(self):
        chars = f"{string.digits}{string.ascii_letters}-_"
        short_link = "".join(choices(chars, k=6))

        link = self.query.filter_by(short_link=short_link).first()
        if link:
            return self.generate_short_link()

        return short_link
