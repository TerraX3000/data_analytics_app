import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# make a sample data frame with 6 columns
np.random.seed(0)
df = pd.DataFrame({"Col " + str(i + 1): np.random.rand(30) for i in range(6)})

layout = html.Div(
    [
        html.Div(
            dcc.Graph(id="g1", config={"displayModeBar": False}),
            className="w3-third",
        ),
        html.Div(
            dcc.Graph(id="g2", config={"displayModeBar": False}),
            className="w3-third",
        ),
        html.Div(
            dcc.Graph(id="g3", config={"displayModeBar": False}),
            className="w3-third",
        ),
    ],
    className="w3-row-padding",
)
