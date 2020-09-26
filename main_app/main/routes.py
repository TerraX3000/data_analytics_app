from flask import render_template, redirect, url_for, flash, request, Blueprint
import matplotlib.pyplot as plt, mpld3
from main_app.main.bokeh_json import make_plot, page

import json
from bokeh.resources import CDN
from bokeh.embed import json_item

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def homePage():
    return render_template("home.html", title="Home")


@main_bp.route("/about")
def aboutPage():
    return render_template("about.html", title="About")


@main_bp.route("/oldplot")
def showPlot():
    # plot = plt.plot([3, 1, 4, 1, 5], "ks-", mec="w", mew=5, ms=20)
    # fig = plot[0].figure

    keys = [1, 2, 3, 4]
    values = [1, 4, 2, 3]

    plt.bar(keys, values, width=0.5)

    #     plt.xlabel("Side Effects")
    #     plt.ylabel("Percentages of Occurence of Side Effects")
    #     plt.title(
    #         "Bar Chart showing Side Effects of Breast \
    # Cancer Medication(s) With Their Corrresponding Percentages Of \
    # Occurence"
    #     )
    # plt.legend()

    # fig = plots[0].figure
    # ax = plots[0].axis

    # plt_html = mpld3.fig_to_html(fig)
    # print(plt_html)
    return render_template("plot.html")


@main_bp.route("/mpld3")
def showMpld3():
    return render_template("mpld3.html")


@main_bp.route("/bokeh")
def showBokeh():
    return render_template("bokeh.html")


@main_bp.route("/dynamicplot")
def showDynamicPlot():
    p = make_plot("petal_width", "petal_length")
    return json.dumps(json_item(p, "myplot"))


@main_bp.route("/iris")
def root():
    # return page.render(resources=CDN.render())
    print(CDN.render())
    return render_template("iris.html", resources=CDN.render())


@main_bp.route("/plot")
def plot():
    p = make_plot("petal_width", "petal_length")
    return json.dumps(json_item(p, "myplot1"))


@main_bp.route("/plot2")
def plot2():
    p = make_plot("sepal_width", "sepal_length")
    return json.dumps(json_item(p))