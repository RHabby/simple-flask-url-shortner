from flask import Blueprint, redirect, render_template, request, url_for

import app.url_shortener.utils as u
from app import db
from app.url_shortener.models import Link

blueprint = Blueprint(name="url_shortener",
                      import_name=__name__, url_prefix="/s")


@blueprint.route("/<short_link>")
def redirect_to_short_url(short_link):
    link = Link.query.filter_by(short_link=short_link).first_or_404()

    link.visits += 1
    db.session.commit()

    return redirect(link.original_link)


@blueprint.route("/")
def index():
    title = "Url Shortener Index Page"
    return render_template("url_shortener/index.html", title=title)


@blueprint.route("/add_link", methods=["POST"])
def add_link():
    title = "Link was shorten"
    original_link = request.form["original_link"]
    validate = u.validate_url(original_link)
    if validate:
        link = Link(original_link=original_link)

        db.session.add(link)
        db.session.commit()
    else:
        return redirect(url_for("url_shortener.index"))

    return render_template("url_shortener/link_added.html",
                           new_link=link.short_link,
                           original_link=link.original_link,
                           title=title)


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
