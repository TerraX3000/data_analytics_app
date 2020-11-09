from main_app import db
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_table

from datetime import datetime

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

df = pd.read_sql_table("dataset_Telematics_Data_6", db.engine, parse_dates=["Date"])
# Convert the date and add new column for day of year which uses integer values suitable for the slider widget
df["dayofyear"] = df["Date"].dt.dayofyear

product_categories = df["Product Category"].unique()
available_indicators = df["Parameter"].unique()


layout = html.Div(
    [
        html.Div(
            [
                html.H1("Data Analysis and Trending"),
                html.P("Perform simple data analysis on simulated telematics data"),
                html.H2("Step 1.  Data Set Review and Selection"),
                html.P(
                    "Use the drop down filters to narrow your analysis based on product category, product, and company."
                ),
                html.P(
                    "The data table lists each company and their product inventory."
                ),
            ],
            className="w3-container",
        ),
        # Table
        html.Div(
            html.Div(
                [
                    dcc.Dropdown(
                        id="table-product-category",
                        value="Asphalt Paver",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="table-product",
                        value="All",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="table-company",
                        value="All",
                        className="w3-text-black w3-padding w3-half",
                    ),
                ],
                className="w3-row-padding",
                # style={"display": "inline-block", "width": "30%"},
            ),
            style={
                "borderTop": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        # html.Div(
        #     [
        #         dcc.Graph(id="company-equipment-table"),
        #     ]
        # ),
        html.Div(
            [
                html.Div(
                    [
                        dash_table.DataTable(
                            id="table",
                            style_cell={
                                "textAlign": "left",
                                "paddingLeft": "15px",
                                "paddingRight": "15px",
                                "backgroundColor": "rgb(250, 250, 250)",
                                "color": "black",
                                "font-family": "sans-serif",
                            },
                            fixed_rows={"headers": True},
                            style_header={"backgroundColor": "rgb(200, 200, 200)"},
                            page_action="none",
                            style_table={"height": "300px", "overflowY": "auto"},
                            style_cell_conditional=[
                                {"if": {"column_id": "Company"}, "width": "200px"},
                            ],
                            style_as_list_view=True,
                        )
                    ],
                    className="w3-container w3-medium",
                )
            ],
        ),
        html.Div(className="w3-panel"),
        # Trending graphs
        html.Div(
            [
                html.H2("Step 2.  View Sensor Time-Series Data"),
                html.P(
                    "The main plot shows the selected parameter as a function of time. "
                ),
                html.P(
                    "Data can be narrowed down by selecting the product name in the legend."
                ),
                html.P("Values are displayed by hovering over data points."),
                html.P(
                    "Selecting a data point will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="multi-line-plot-variable",
                    options=[{"label": i, "value": i} for i in available_indicators],
                    value="Fuel Usage",
                    className="w3-text-black w3-padding w3-quarter",
                ),
            ],
            className="w3-row-padding",
        ),
        html.Div(
            [
                dcc.Graph(
                    id="multi-line-plot",
                    clickData={"points": [{"customdata": [0, "gph"]}]},
                    hoverData={"points": [{"customdata": [0, "gph"]}]},
                    className="w3-half",
                ),
                html.Div(
                    [dcc.Graph(id="param-01-plot"), dcc.Graph(id="param-02-plot")],
                    # style={"display": "inline-block", "width": "51%"},
                    className="w3-half",
                ),
            ],
            className="w3-row-padding",
        ),
        # html.Div(
        #     [dcc.Graph(id="param-01-plot"), dcc.Graph(id="param-02-plot")],
        #     # style={"display": "inline-block", "width": "51%"},
        #     className="w3-half",
        # ),
        html.Div(
            [
                html.H2("Step 3.  View Sparkline Plots for Categorized Data Sets"),
                html.P(
                    "Sparkline plots show trending data for data in different categories."
                ),
                html.P("Values are displayed by hovering over data points."),
                html.P(
                    "Selecting a sparkline will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        # Sparkline graphs
        # html.Div(
        #     [
        #         dcc.Graph(
        #             id="sparkline-group-plot",
        #             config=dict(displayModeBar=False),
        #             className="w3-panel",
        #         ),
        #     ]
        # ),
        html.Div(
            [
                dcc.Graph(
                    id="sparkline-01-plot",
                    config=dict(displayModeBar=False),
                    className="w3-cell",
                ),
                dcc.Graph(
                    id="sparkline-02-plot",
                    config=dict(displayModeBar=False),
                    className="w3-cell",
                ),
                dcc.Graph(
                    id="sparkline-03-plot",
                    config=dict(displayModeBar=False),
                    className="w3-cell",
                ),
                dcc.Graph(
                    id="sparkline-04-plot",
                    config=dict(displayModeBar=False),
                    className="w3-cell",
                ),
            ],
            className="w3-cell-row",
        ),
        html.Div(className="w3-panel"),
        html.Div(
            [
                html.H2("Step 4.  Create Cross-Filter Plots"),
                html.P("Choose sensor data types to plot on the X and Y axes."),
                html.P("Values are displayed by hovering over data points."),
                html.P(
                    "Selecting a data point will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        # Cross-filter graphs
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="crossfilter-xaxis-column",
                            options=[
                                {"label": i, "value": i} for i in available_indicators
                            ],
                            value="Fuel Usage",
                            className="w3-text-black",
                        ),
                        dcc.RadioItems(
                            id="crossfilter-xaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                            className="w3-padding",
                        ),
                    ],
                    className="w3-half w3-padding-16",
                ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="crossfilter-yaxis-column",
                            options=[
                                {"label": i, "value": i} for i in available_indicators
                            ],
                            value="Distance",
                            className="w3-text-black",
                        ),
                        dcc.RadioItems(
                            id="crossfilter-yaxis-type",
                            options=[
                                {"label": i, "value": i} for i in ["Linear", "Log"]
                            ],
                            value="Linear",
                            labelStyle={"display": "inline-block"},
                            className="w3-padding",
                        ),
                    ],
                    className="w3-half w3-padding-16",
                ),
            ],
            className="w3-row-padding w3-panel w3-light-gray",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="crossfilter-indicator-scatter",
                            hoverData={
                                "points": [
                                    {
                                        "customdata": "Hollis & Hollis Group Inc (Clarksville, TN)"
                                    }
                                ]
                            },
                        ),
                        dcc.Slider(
                            id="crossfilter-year--slider",
                            min=df["dayofyear"].min(),
                            max=df["dayofyear"].max(),
                            value=df["dayofyear"].max(),
                            marks={
                                str(dayofyear): str(dayofyear)
                                for dayofyear in df["dayofyear"].unique()
                            },
                            step=None,
                            className="w3-margin-left",
                        ),
                    ],
                    className="w3-half",
                ),
                html.Div(
                    [
                        dcc.Graph(id="x-time-series"),
                        dcc.Graph(id="y-time-series"),
                    ],
                    className="w3-half",
                ),
            ],
            className="w3-row-padding",
        ),
        html.Div(className="w3-panel"),
        html.Div(
            [
                html.H2("Step 5.  Parallel Categories Diagram"),
                html.P(
                    "The parallel categories diagram (also known as parallel sets or alluvial diagram) is a visualization of multi-dimensional categorical data sets. Each variable in the data set is represented by a column of rectangles, where each rectangle corresponds to a discrete value taken on by that variable. The relative heights of the rectangles reflect the relative frequency of occurrence of the corresponding value."
                ),
                html.P(
                    "Combinations of category rectangles across dimensions are connected by ribbons, where the height of the ribbon corresponds to the relative frequency of occurrence of the combination of categories in the data set."
                ),
                html.P(
                    "Use the drop down filters to narrow your analysis based on product category, product, and company."
                ),
                html.P(
                    "The plot will display the number of products matching the category values of product category, product, purchase type, and age.  The colors correspond to the product's age as shown in the legend."
                ),
                html.P(
                    "Values are displayed by hovering over rectangles or their connecting ribbons."
                ),
            ],
            className="w3-container",
        ),
        html.Div(
            html.Div(
                [
                    dcc.Dropdown(
                        id="parallel-categories-product-category",
                        value="Asphalt Paver",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="parallel-categories-product",
                        value="All",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="parallel-categories-company",
                        value="All",
                        className="w3-text-black w3-padding w3-half",
                    ),
                ],
                className="w3-row-padding",
                # style={"display": "inline-block", "width": "30%"},
            ),
            style={
                "borderTop": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        html.Div(
            [dcc.Graph(id="parallel-categories-plot")],
            className="w3-container w3-margin",
        ),
        html.Div(
            [
                html.H2("Step 6.  Dataset Mapping"),
                html.P(
                    "The map view shows the location of companies and their products as circles."
                ),
                html.P(
                    "Use the drop down filters to narrow your analysis based on product category, product, and company."
                ),
                html.P(
                    "The color of circle corresponds to the product type.  The size of the circle corresponds to the product age."
                ),
                html.P("Values are displayed by hovering over the circles."),
            ],
            className="w3-container",
        ),
        html.Div(
            html.Div(
                [
                    dcc.Dropdown(
                        id="map-category",
                        value="Asphalt Paver",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="map-product",
                        value="All",
                        className="w3-text-black w3-padding w3-quarter",
                    ),
                    dcc.Dropdown(
                        id="map-company",
                        value="All",
                        className="w3-text-black w3-padding w3-half",
                    ),
                ],
                className="w3-row-padding",
                # style={"display": "inline-block", "width": "30%"},
            ),
            style={
                "borderTop": "thin lightgrey solid",
                "backgroundColor": "rgb(250, 250, 250)",
                "padding": "10px 5px",
            },
        ),
        html.Div(
            [dcc.Graph(id="map-plot")],
            className="w3-container w3-margin",
        ),
    ]
)
