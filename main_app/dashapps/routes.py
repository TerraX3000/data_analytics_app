from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    Blueprint,
    current_app,
)
import dash
import dash_html_components as html

dashapps_bp = Blueprint("dashapps_bp", __name__)


@dashapps_bp.route("/dashsamples")
def showDashSamples():
    return render_template("dash.html", title="Data Visualization with Dash")
