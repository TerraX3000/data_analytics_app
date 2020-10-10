from flask import current_app
import os

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column, row
from bokeh.models import Slider, ColumnDataSource, CustomJS
from bokeh.util.hex import axial_to_cartesian, hexbin
from bokeh.transform import linear_cmap
from bokeh.palettes import Spectral4
import bokeh.sampledata

# bokeh.sampledata.download()
from bokeh.sampledata.iris import flowers

# from bokeh.sampledata.stocks import AAPL
import numpy as np
from math import pi
import pandas as pd
from random import random


def irisPlot(x, y):
    colormap = {"setosa": "red", "versicolor": "green", "virginica": "blue"}
    colors = [colormap[x] for x in flowers["species"]]
    p = figure(
        title="Iris Morphology", sizing_mode="fixed", plot_width=400, plot_height=400
    )
    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    p.circle(flowers[x], flowers[y], color=colors, fill_alpha=0.2, size=10)
    return p


def simplePlot():
    # prepare some data
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]

    # create a new plot with a title and axis labels
    p = figure(
        title="Simple Line Example",
        x_axis_label="x",
        y_axis_label="y",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label="Temp.", line_width=2)

    # show the results
    return p


def logAxisPlot():
    # prepare some data
    x = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    y0 = [i ** 2 for i in x]
    y1 = [10 ** i for i in x]
    y2 = [10 ** (i ** 2) for i in x]
    # create a new plot
    p = figure(
        title="Log Axis Example",
        tools="pan,box_zoom,reset,save",
        y_axis_type="log",
        y_range=[0.001, 10 ** 11],
        x_axis_label="sections",
        y_axis_label="particles",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    # add some renderers
    p.line(x, x, legend_label="y=x")
    p.circle(x, x, legend_label="y=x", fill_color="white", size=8)
    p.line(x, y0, legend_label="y=x^2", line_width=3)
    p.line(x, y1, legend_label="y=10^x", line_color="red")
    p.circle(x, y1, legend_label="y=10^x", fill_color="red", line_color="red", size=6)
    p.line(x, y2, legend_label="y=10^x^2", line_color="orange", line_dash="4 4")

    return p


def sliderPlot():
    plot = figure(
        title="Adjustable Radius Slider Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    r = plot.circle(
        [
            1,
            2,
            3,
            4,
            5,
        ],
        [3, 2, 5, 6, 4],
        radius=0.2,
        alpha=0.5,
    )

    slider = Slider(start=0.1, end=2, step=0.01, value=0.2)
    slider.js_link("value", r.glyph, "radius")
    return column(plot, slider)


def plotColorsAndSizes():
    # prepare some data
    N = 4000
    x = np.random.random(size=N) * 100
    y = np.random.random(size=N) * 100
    radii = np.random.random(size=N) * 1.5
    colors = [
        "#%02x%02x%02x" % (int(r), int(g), 150) for r, g in zip(50 + 2 * x, 30 + 2 * y)
    ]
    TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
    # create a new plot with the tools above, and explicit ranges
    p = figure(
        title="Colors and Sizes",
        tools=TOOLS,
        x_range=(0, 100),
        y_range=(0, 100),
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    # add a circle renderer with vectorized colors and sizes
    p.circle(x, y, radius=radii, fill_color=colors, fill_alpha=0.6, line_color=None)
    return p


def stepLinePlot():
    p = figure(
        title="Step Line Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    # add a steps renderer
    p.step([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], line_width=2, mode="center")
    return p


def multipleLinesPlot():
    p = figure(
        title="Multiple Lines Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    p.multi_line(
        [[1, 3, 2], [3, 4, 6, 6]],
        [[2, 1, 4], [4, 7, 8, 5]],
        color=["firebrick", "navy"],
        alpha=[0.8, 0.3],
        line_width=4,
    )
    return p


def missingPointsPlot():
    p = figure(
        title="Missing Points Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    # add a line renderer with a NaN
    nan = float("nan")
    p.line([1, 2, 3, nan, 4, 5], [6, 7, 2, 4, 4, 5], line_width=2)
    return p


def stackedLinesPlot():
    p = figure(
        title="Stacked Lines Plot", sizing_mode="fixed", plot_width=400, plot_height=400
    )
    source = ColumnDataSource(
        data=dict(
            x=[1, 2, 3, 4, 5],
            y1=[1, 2, 4, 3, 4],
            y2=[1, 4, 2, 2, 3],
        )
    )
    p.vline_stack(["y1", "y2"], x="x", source=source)
    return p


def vbarPlot():
    p = figure(
        title="Vertical Bar Plot", sizing_mode="fixed", plot_width=400, plot_height=400
    )
    p.vbar(x=[1, 2, 3], width=0.5, bottom=0, top=[1.2, 2.5, 3.7], color="firebrick")
    return p


def hbarPlot():
    p = figure(
        title="Horizontal Bar Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    p.hbar(y=[1, 2, 3], height=0.5, left=0, right=[1.2, 2.5, 3.7], color="navy")
    return p


def stackedBarPlot():
    p = figure(
        title="Stacked Bar Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    source = ColumnDataSource(
        data=dict(
            y=[1, 2, 3, 4, 5],
            x1=[1, 2, 4, 3, 4],
            x2=[1, 4, 2, 2, 3],
        )
    )
    p.hbar_stack(
        ["x1", "x2"], y="y", height=0.8, color=("grey", "lightgrey"), source=source
    )
    return p


def rectanglesPlot():
    p = figure(
        title="Rectangles Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    p.quad(
        top=[2, 3, 4],
        bottom=[1, 2, 3],
        left=[1, 2, 3],
        right=[1.2, 2.5, 3.7],
        color="#B3DE69",
    )
    return p


def rotatedRectanglesPlot():
    p = figure(
        title="Rotated Rectangles Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    p.rect(
        x=[1, 2, 3],
        y=[1, 2, 3],
        width=0.2,
        height=40,
        color="#CAB2D6",
        angle=pi / 3,
        height_units="screen",
    )
    return p


def hexTilePlot():
    p = figure(
        title="Hex Tiles Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
        toolbar_location=None,
    )
    q = np.array([0, 0, 0, -1, -1, 1, 1])
    r = np.array([0, -1, 1, 0, 1, -1, 0])
    p.grid.visible = False

    p.hex_tile(
        q,
        r,
        size=1,
        fill_color=["firebrick"] * 3 + ["navy"] * 4,
        line_color="white",
        alpha=0.5,
    )

    x, y = axial_to_cartesian(q, r, 1, "pointytop")

    p.text(
        x,
        y,
        text=["(%d, %d)" % (q, r) for (q, r) in zip(q, r)],
        text_baseline="middle",
        text_align="center",
    )
    return p


def hexBinPlot():
    p = figure(
        title="Hex Bin Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
        tools="wheel_zoom,reset",
        match_aspect=True,
        background_fill_color="#440154",
    )

    n = 50000
    x = np.random.standard_normal(n)
    y = np.random.standard_normal(n)

    bins = hexbin(x, y, 0.1)

    p.grid.visible = False

    p.hex_tile(
        q="q",
        r="r",
        size=0.1,
        line_color=None,
        source=bins,
        fill_color=linear_cmap("counts", "Viridis256", 0, max(bins.counts)),
    )
    return p


def directedAreaPlot():
    p = figure(
        title="Directed Area Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )

    p.varea(x=[1, 2, 3, 4, 5], y1=[2, 6, 4, 3, 5], y2=[1, 4, 2, 2, 3])
    return p


def stackedAreaPlot():
    p = figure(
        title="Stacked Area Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )
    source = ColumnDataSource(
        data=dict(
            x=[1, 2, 3, 4, 5],
            y1=[1, 2, 4, 3, 4],
            y2=[1, 4, 2, 2, 3],
        )
    )
    p = figure(plot_width=400, plot_height=400)

    p.varea_stack(["y1", "y2"], x="x", color=("grey", "lightgrey"), source=source)
    return p


def colorMappedImagePlot():
    p = figure(
        title="Color Mapped Image Plot",
        sizing_mode="fixed",
        plot_width=400,
        plot_height=400,
    )

    x = np.linspace(0, 10, 250)
    y = np.linspace(0, 10, 250)
    xx, yy = np.meshgrid(x, y)
    d = np.sin(xx) * np.cos(yy)

    p.x_range.range_padding = p.y_range.range_padding = 0

    p.image(image=[d], x=0, y=0, dw=10, dh=10, palette="Spectral11", level="image")
    p.grid.grid_line_width = 0.5
    return p


def dateTimePlot():
    p = figure(
        title="Date Time Axes Plot",
        sizing_mode="fixed",
        plot_width=800,
        plot_height=400,
        x_axis_type="datetime",
    )
    # df = pd.DataFrame(AAPL)
    file_path = os.path.join(
        current_app.root_path, "static/bokeh_sample_data", "AAPL.csv"
    )
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"])
    p.line(df["Date"], df["Close"], color="navy", alpha=0.5)
    return p


def interactiveLegend():
    p = figure(plot_width=800, plot_height=400, x_axis_type="datetime")
    p.title.text = "Click on legend entries to mute the corresponding lines"
    file_path = os.path.join(
        current_app.root_path, "static/bokeh_sample_data", "AAPL.csv"
    )
    aapl = pd.read_csv(file_path)
    file_path = os.path.join(
        current_app.root_path, "static/bokeh_sample_data", "IBM.csv"
    )
    ibm = pd.read_csv(file_path)
    file_path = os.path.join(
        current_app.root_path, "static/bokeh_sample_data", "MSFT.csv"
    )
    msft = pd.read_csv(file_path)
    file_path = os.path.join(
        current_app.root_path, "static/bokeh_sample_data", "GOOG.csv"
    )
    goog = pd.read_csv(file_path)

    for data, name, color in zip(
        [aapl, ibm, msft, goog], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4
    ):
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])
        p.line(
            df["Date"],
            df["Close"],
            line_width=2,
            color=color,
            alpha=0.8,
            muted_color=color,
            muted_alpha=0.2,
            legend_label=name,
        )

    p.legend.location = "top_left"
    p.legend.click_policy = "mute"

    return p


def sliderPowerPlot():
    x = [x * 0.005 for x in range(0, 200)]
    y = x

    source = ColumnDataSource(data=dict(x=x, y=y))

    p = figure(plot_width=400, plot_height=370)
    p.line("x", "y", source=source, line_width=3, line_alpha=0.6)

    callback = CustomJS(
        args=dict(source=source),
        code="""
        var data = source.data;
        var f = cb_obj.value
        var x = data['x']
        var y = data['y']
        for (var i = 0; i < x.length; i++) {
            y[i] = Math.pow(x[i], f)
        }
        source.change.emit();
    """,
    )
    slider = Slider(start=0.1, end=4, value=1, step=0.1, title="power")
    slider.js_on_change("value", callback)
    layout = column(slider, p)
    return layout


def transferSelection():
    x = [random() for x in range(500)]
    y = [random() for y in range(500)]

    s1 = ColumnDataSource(data=dict(x=x, y=y))
    p1 = figure(
        plot_width=400, plot_height=400, tools="lasso_select", title="Select Here"
    )
    p1.circle("x", "y", source=s1, alpha=0.6)

    s2 = ColumnDataSource(data=dict(x=[], y=[]))
    p2 = figure(
        plot_width=400,
        plot_height=400,
        x_range=(0, 1),
        y_range=(0, 1),
        tools="",
        title="Watch Here",
    )
    p2.circle("x", "y", source=s2, alpha=0.6)
    s1.selected.js_on_change(
        "indices",
        CustomJS(
            args=dict(s1=s1, s2=s2),
            code="""
            var inds = cb_obj.indices;
            var d1 = s1.data;
            var d2 = s2.data;
            d2['x'] = []
            d2['y'] = []
            for (var i = 0; i < inds.length; i++) {
                d2['x'].push(d1['x'][inds[i]])
                d2['y'].push(d1['y'][inds[i]])
            }
            s2.change.emit();
        """,
        ),
    )
    layout = row(p1, p2)
    return layout