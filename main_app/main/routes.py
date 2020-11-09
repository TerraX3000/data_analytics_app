from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
)
from main_app.main.utilityfunctions import printLogEntry

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def homePage():
    printLogEntry("Displaying home page")
    return render_template("home.html", title="Home")


@main_bp.route("/about")
def aboutPage():
    return render_template("about.html", title="About")


@main_bp.route("/portfolio")
def displayPortfolio():
    printLogEntry("Displaying portfolio")
    return render_template("portfolio.html", title="Personal Portfolio")


@main_bp.route("/resume")
def displayResume():
    printLogEntry("Displaying resume")
    return render_template("resume.html", title="Resume")


@main_bp.route("/telematics")
def displayTelematics():
    printLogEntry("Displaying telematics")
    return render_template("telematics.html", title="Telematics Analysis Demo Overview")
