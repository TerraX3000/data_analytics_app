from main_app import db
from main_app.models import DatasetManager
from main_app.main.referenceData import getDatasetNames
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from pandas.api.types import is_numeric_dtype


def setDropdownChoices():
    df = pd.read_sql_table("dataset_Telematics_Data_3", db.engine)
    columns = df.columns.to_list()
    choices = []
    for columnName in columns:
        if is_numeric_dtype(df[columnName]):
            choices.append(columnName)
    options = [{"label": i, "value": i} for i in choices]
    return options


layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="xaxis-column",
                    options=setDropdownChoices(),
                    value="Ops Time",
                    placeholder="Select column for x-axis",
                    className="w3-text-black w3-padding",
                ),
                dcc.RadioItems(
                    id="xaxis-type",
                    options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                    value="Linear",
                    labelStyle={"display": "inline-block"},
                    className="w3-padding",
                ),
            ],
            style={"width": "48%", "display": "inline-block"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="yaxis-column",
                    options=setDropdownChoices(),
                    value="Value",
                    placeholder="Select column for y-axis",
                    className="w3-text-black w3-padding",
                ),
                dcc.RadioItems(
                    id="yaxis-type",
                    options=[{"label": i, "value": i} for i in ["Linear", "Log"]],
                    value="Linear",
                    labelStyle={"display": "inline-block"},
                    className="w3-padding",
                ),
            ],
            style={"width": "48%", "float": "right", "display": "inline-block"},
        ),
        dcc.Graph(id="simple scatter plot", className="w3-padding"),
    ],
)


def register_callbacks(app):
    @app.callback(
        Output("simple scatter plot", "figure"),
        [
            Input("xaxis-column", "value"),
            Input("yaxis-column", "value"),
            Input("xaxis-type", "value"),
            Input("yaxis-type", "value"),
        ],
    )
    def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type):
        df = pd.read_sql_table("dataset_Telematics_Data_3", db.engine)

        fig = px.scatter(
            df,
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            hover_name=df["Equipment"],
            color="Company",
        )

        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )

        fig.update_xaxes(
            title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
        )

        fig.update_yaxes(
            title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
        )

        return fig
