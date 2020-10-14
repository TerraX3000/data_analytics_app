import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df = pd.read_csv("https://plotly.github.io/datasets/country_indicators.csv")

available_indicators = df["Indicator Name"].unique()

layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="crossfilter-xaxis-column",
                            options=[
                                {"label": i, "value": i} for i in available_indicators
                            ],
                            value="Electric power consumption (kWh per capita)",
                        ),
                        dcc.RadioItems(
                            id="crossfilter-xaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                        ),
                    ],
                    style={"width": "49%", "display": "inline-block"},
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="crossfilter-yaxis-column",
                            options=[
                                {"label": i, "value": i} for i in available_indicators
                            ],
                            value="GDP growth (annual %)",
                        ),
                        dcc.RadioItems(
                            id="crossfilter-yaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                        ),
                    ],
                    style={"width": "49%", "float": "right", "display": "inline-block"},
                ),
            ],
            style={
                "borderBottom": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="crossfilter-indicator-scatter",
                    hoverData={"points": [{"customdata": "Japan"}]},
                )
            ],
            style={"width": "49%", "display": "inline-block", "padding": "0 20"},
        ),
        html.Div(
            [
                dcc.Graph(id="x-time-series"),
                dcc.Graph(id="y-time-series"),
            ],
            style={"display": "inline-block", "width": "49%"},
        ),
        html.Div(
            [
                html.Div(
                    dcc.Slider(
                        id="crossfilter-year--slider",
                        min=df["Year"].min(),
                        max=df["Year"].max(),
                        value=df["Year"].max(),
                        marks={str(year): str(year) for year in df["Year"].unique()},
                        step=None,
                    ),
                    style={
                        "width": "49%",
                        "padding": "0px 20px 20px 20px",
                        "backgroundColor": "rgb(250, 250, 250)",
                    },
                ),
            ],
            style={"display": "inline", "width": "100%"},
        ),
    ]
)