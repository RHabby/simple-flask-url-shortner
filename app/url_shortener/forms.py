from urllib.parse import urlparse

import requests
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from app.url_shortener.models import Link


def validate_url(form, original_link):
    original_link = original_link.data.strip()

    parsed_url = urlparse(original_link)
    scheme = parsed_url.scheme
    domain = parsed_url.netloc

    if not all([scheme, domain]):
        if scheme == "":
            original_link = f"https://{original_link}"
            raise ValidationError(
                f"Может быть попробовать так: {original_link}?")
        raise ValidationError(f"Некорректный домен: {domain}.")

    r = requests.get(original_link)
    status = r.status_code
    print(scheme, domain, original_link, status)

    if str(status).startswith("3"):
        raise ValidationError(
            f"Ваша ссылка ведет на {r.headers['Location']}. Попробуйте вставить эту ссылку.")
    if status != 200:
        raise ValidationError("Ваша ссылка не работает.")


def validate_short_link(form, custom_short_link):
    short_link = Link.query.filter_by(
        short_link=custom_short_link.data).first()
    if short_link:
        raise ValidationError("Придумайте другой идентификатор.")


class ShortenerForm(FlaskForm):
    original_link = StringField(
        label="Original Link",
        validators=[DataRequired(), validate_url],
        render_kw={
            "class": "original-link",
            "placeholder": "Your link here",
        }
    )
    custom_short_link = StringField(
        label="Custom Short Link",
        validators=[Length(max=10), validate_short_link],
        render_kw={
            "id": "custom-link",
            "class": "custom-link",
            "placeholder": "Your short link",
            "style": "visibility: hidden",
        }
    )
    is_custom_short_link = BooleanField(
        label="Custom Short Link",
        default=False,
        render_kw={
            "class": "is-custom-checkbox",
            "id": "customShortLink",
            "onclick": "showCustomLinkField('custom-link', 'shorten-btn')",
        }
    )
    submit = SubmitField(
        label="Shorten",
        render_kw={"class": "shorten-btn btn-short", "id": "shorten-btn"}
    )
