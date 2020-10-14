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


# df = pd.DataFrame(
#     {
#         "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#         "Amount": [4, 1, 2, 2, 4, 5],
#         "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
#     }
# )
# # Define barchart
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# # Create Layout
# layout = html.Div(
#     [
#         dcc.Graph(id="example-graph", figure=fig),
#     ]
# )


datasetNames = getDatasetNames()
options = []

layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="dataset-id",
                    options=[{"label": i[1], "value": i[0]} for i in datasetNames],
                    placeholder="Select dataset to plot",
                    className="w3-text-black w3-padding",
                ),
            ],
            style={"width": "48%", "display": "block"},
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="xaxis-column",
                    options=[{"label": i, "value": i} for i in options],
                    placeholder="Select column for bar chart",
                    className="w3-text-black w3-padding",
                ),
            ],
            style={"width": "48%", "display": "inline-block"},
        ),
        dcc.Graph(id="simple bar chart", className="w3-padding"),
    ],
)


def register_callbacks(app):
    @app.callback(
        Output("xaxis-column", "options"),
        Input("dataset-id", "value"),
    )
    def updateDropdownOptions(dataset_id):
        log = DatasetManager.query.get_or_404(dataset_id)
        datasetSqlName = log.datasetSqlName
        df = pd.read_sql_table(datasetSqlName, db.engine)
        columns = df.columns.to_list()
        choices = []
        for columnName in columns:
            # if df[columnName].dtype == np.float64 or df[columnName].dtype == np.int64:
            if df[columnName].dtype != np.float64:
                # if not is_numeric_dtype(df[columnName]):
                choices.append(columnName)
        options = [{"label": i, "value": i} for i in choices]
        return options

    @app.callback(
        Output("simple bar chart", "figure"),
        [
            Input("dataset-id", "value"),
            Input("xaxis-column", "value"),
        ],
    )
    def update_graph(dataset_id, xaxis_column_name):
        print("Running update_graph for bar chart")
        log = DatasetManager.query.get_or_404(dataset_id)
        datasetSqlName = log.datasetSqlName
        df = pd.read_sql_table(datasetSqlName, db.engine)
        # Simple scatter plot
        # fig = px.scatter(x=Fare, y=Age)

        # fig = px.scatter(
        #     x=df[xaxis_column_name],
        #     y=df[yaxis_column_name],
        #     hover_name=df[yaxis_column_name],
        # )

        vc = df[xaxis_column_name].value_counts()
        categories = vc.index.to_list()
        # Categorical values can also be used as coordinates
        values = vc.to_list()
        print("categories=", categories)
        print("values=", values)
        # fig = px.bar(df, x=categories, y=values, color="City", barmode="group")
        fig = px.bar(df, x=categories, y=values)

        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )

        fig.update_xaxes(
            title=xaxis_column_name,
        )

        fig.update_yaxes(
            title="Count",
        )

        return fig