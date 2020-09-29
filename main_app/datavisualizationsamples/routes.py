from flask import render_template, redirect, url_for, flash, request, Blueprint
from main_app.datavisualizationsamples.datavizsamples import (
    irisPlot,
    simplePlot,
    logAxisPlot,
    sliderPlot,
    plotColorsAndSizes,
    stepLinePlot,
    multipleLinesPlot,
    missingPointsPlot,
    stackedLinesPlot,
    vbarPlot,
    hbarPlot,
    stackedBarPlot,
    rectanglesPlot,
    rotatedRectanglesPlot,
    hexTilePlot,
    hexBinPlot,
    directedAreaPlot,
    stackedAreaPlot,
    colorMappedImagePlot,
    dateTimePlot,
)

import json
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import gridplot, layout, Spacer

datavisualizationsamples_bp = Blueprint("datavisualizationsamples_bp", __name__)


@datavisualizationsamples_bp.route("/datavisualizationsamples")
def showDataVisualizationSamples():
    return render_template(
        "datavisualizationsamples.html",
        resources=CDN.render(),
        title="Data Visualization Samples",
    )


@datavisualizationsamples_bp.route("/gridplot")
def showGridPlot():
    # Create plots
    p1 = irisPlot("petal_width", "petal_length")
    p2 = irisPlot("sepal_width", "sepal_length")
    p3 = simplePlot()
    p4 = logAxisPlot()
    p5 = sliderPlot()
    p6 = plotColorsAndSizes()
    p7 = stepLinePlot()
    p8 = multipleLinesPlot()
    p9 = missingPointsPlot()
    p10 = stackedLinesPlot()
    p11 = vbarPlot()
    p12 = hbarPlot()
    p13 = rectanglesPlot()
    p14 = rotatedRectanglesPlot()
    p15 = hexTilePlot()
    p16 = hexBinPlot()
    p17 = directedAreaPlot()
    p18 = stackedAreaPlot()
    p19 = colorMappedImagePlot()
    p20 = dateTimePlot()

    # Define column and row spacers
    # Spacer: margin - property type: Tuple ( Int , Int , Int , Int )
    # Allows to create additional space around the component.
    # The values in the tuple are ordered as follows - Margin-Top, Margin-Right, Margin-Bottom and Margin-Left
    sp1 = Spacer(margin=(10, 10, 10, 10))
    sp2 = Spacer(margin=(10, 10, 10, 10))
    rowsp = Spacer(margin=(10, 800, 10, 800))

    # Create a grid layout of plots
    plotLayout = layout(
        [
            [p1, sp1, p2, sp2, p3],
            [rowsp],
            [p4, sp1, p5, sp2, p6],
            [rowsp],
            [p7, sp1, p8, sp2, p9],
            [rowsp],
            [p10, sp1, p11, sp2, p12],
            [rowsp],
            [p13, sp1, p14, sp2, p15],
            [rowsp],
            [p16, sp1, p17, sp2, p18],
            [rowsp],
            [p19, sp1, p20],
            [rowsp],
        ]
    )
    return json.dumps(json_item(plotLayout))