import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

layout = html.Div(
    [
        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div(
            [
                "Input: ",
                dcc.Input(id="my-input", value="initial value", type="text"),
            ]
        ),
        html.Br(),
        html.Div(id="my-output"),
    ]
)