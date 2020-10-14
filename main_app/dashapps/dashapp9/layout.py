from main_app import db
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


df = pd.read_sql_table("dataset_Titanic_Dataset", db.engine)
df["Pclass"] = df["Pclass"].astype(str)

fig_scatter = px.scatter(
    df,
    x="Fare",
    y="Age",
    size="SibSp",
    color="Pclass",
    hover_name="Name",
    hover_data=["Sex", "Survived"],
    category_orders={"Pclass": ["1", "2", "3"]},
    log_x=False,
    size_max=60,
)


Fare = df["Fare"]
Age = df["Age"]

fig_markers = go.Figure()
# Add traces
fig_markers.add_trace(go.Scatter(x=Fare, y=Age, mode="markers", name="markers"))
fig_markers.add_trace(
    go.Scatter(x=Fare, y=Age, mode="lines+markers", name="lines+markers")
)
fig_markers.add_trace(go.Scatter(x=Fare, y=Age, mode="lines", name="lines"))


layout = html.Div(
    children=[
        html.H1(children="Dataset Plot"),
        html.Div(
            children="""
    This dataset plot is created with Dash.
"""
        ),
        dcc.Graph(id="age-vs-fare", figure=fig_scatter),
        dcc.Graph(id="age-vs-fare-markers", figure=fig_markers),
    ]
)