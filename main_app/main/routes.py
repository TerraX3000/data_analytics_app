from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
)

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def homePage():
    return render_template("home.html", title="Home")


@main_bp.route("/about")
def aboutPage():
    return render_template("about.html", title="About")


@main_bp.route("/portfolio")
def displayPortfolio():
    return render_template("portfolio.html", title="Personal Portfolio")
