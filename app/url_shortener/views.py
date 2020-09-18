from flask import Blueprint, redirect, render_template, url_for, flash

from app import db
from app.url_shortener.forms import ShortenerForm
from app.url_shortener.models import Link

blueprint = Blueprint(name="url_shortener",
                      import_name=__name__)


@blueprint.route("/<short_link>")
def redirect_to_short_url(short_link):
    link = Link.query.filter_by(short_link=short_link).first_or_404()

    link.visits += 1
    db.session.commit()

    return redirect(link.original_link)


@blueprint.route("/")
def index():
    title = "Url Shortener Index Page"
    shortener_form = ShortenerForm()
    return render_template(
        "url_shortener/index.html",
        title=title, form=shortener_form)


@blueprint.route("/add_link", methods=["POST"])
def add_link():
    title = "Link was shorten"
    shortener_form = ShortenerForm()

    if shortener_form.validate_on_submit():

        original_link = shortener_form.original_link.data.strip()
        short_link = shortener_form.custom_short_link.data.strip()

        link = Link(original_link=original_link,
                    short_link=short_link)
        db.session.add(link)
        db.session.commit()

        return render_template("url_shortener/link_added.html",
                               new_link=link.short_link,
                               original_link=link.original_link,
                               title=title)
    else:
        for field, errors in shortener_form.errors.items():
            for error in errors:
                flash(f"{error}")
        return redirect(url_for("url_shortener.index"))


@blueprint.route("/delete-link/<short_link>", methods=["POST"])
def delete_link(short_link):
    link = Link.query.filter_by(short_link=short_link).first()

    db.session.delete(link)
    db.session.commit()

    return redirect(url_for("url_shortener.statistics"))


@blueprint.route("/statistics")
def statistics():
    title = "Some Statistics"
    stats = Link.query.all()
    return render_template("url_shortener/statistics.html",
                           stats=stats, title=title)
