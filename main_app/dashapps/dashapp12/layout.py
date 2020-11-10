from main_app import db
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_table

from datetime import datetime

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

print("Initializing layout for telematics")
try:
    df = pd.read_sql_table("dataset_Telematics_Data_6", db.engine, parse_dates=["Date"])
    print("Using telematics file from MySQL database")
except:
    df = pd.read_csv(
        "main_app/static/data/sample_telematics_data.csv",
        parse_dates=["Date"],
    )
    print(
        "Unable to find telematics file in MySQL database. Using built-in sample_telematics_data.csv file instead"
    )

# Convert the date and add new column for day of year which uses integer values suitable for the slider widget
df["dayofyear"] = df["Date"].dt.dayofyear

product_categories = df["Product Category"].unique()
available_indicators = df["Parameter"].unique()


def insertDropDownMenus(idPrefix):
    print("Inserting dropdown menu for", idPrefix)
    dropDownSelections = html.Div(
        html.Div(
            [
                dcc.Dropdown(
                    id=idPrefix + "-product-category",
                    value="Asphalt Screed",
                    className="w3-text-black w3-padding w3-quarter",
                ),
                dcc.Dropdown(
                    id=idPrefix + "-product",
                    value="All",
                    className="w3-text-black w3-padding w3-quarter",
                ),
                dcc.Dropdown(
                    id=idPrefix + "-company",
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
    )
    return dropDownSelections


layout = html.Div(
    [
        html.Div(
            [
                html.H1("Data Analysis and Trending"),
                html.P("Perform simple data analysis on simulated telematics data"),
                html.H2("Example 1.  Data Set Review"),
                html.P(
                    "Use the drop down filters to tailor your analysis based on product category, product, and company."
                ),
                html.P(
                    "The data table lists each company and their product inventory."
                ),
            ],
            className="w3-container",
        ),
        # Table
        insertDropDownMenus("table"),
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
                html.H2("Example 2.  View Sensor Time-Series Data"),
                html.P(
                    "The main plot shows the selected parameter as a function of time. "
                ),
                html.P(
                    "Data can be narrowed down by double-clicking the product name in the legend."
                ),
                html.P("Values are displayed by hovering over data points."),
                html.P(
                    "Selecting a data point will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        insertDropDownMenus("multi-line"),
        html.Div(
            [
                dcc.Dropdown(
                    id="multi-line-plot-variable",
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
                html.H2("Example 3.  View Sparkline Plots for Sensor Categories"),
                html.P(
                    "Sparkline plots show trending data for different sensor categories."
                ),
                html.P(
                    "Click on a line in the time-series plot (Example 2) to create a new sparkline plot."
                ),
                html.P(
                    "View the values by hovering over data points in the sparkline plots."
                ),
                html.P(
                    "Selecting a sparkline will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        # Create title line for the sparkline plots to identify the selected dataset
        html.Div(
            dcc.Markdown(
                id="sparkline-selection-title",
                className="w3-container w3-small",
            ),
        ),
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
                html.H2("Example 4.  Create Cross-Filter Plots"),
                html.P("Choose sensor data types to plot on the X and Y axes."),
                html.P("Values are displayed by hovering over data points."),
                html.P(
                    "Selecting a data point will update the adjacent sub-plots with data curves for the specific product."
                ),
            ],
            className="w3-container",
        ),
        # Cross-filter graphs
        insertDropDownMenus("cross-filter"),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Dropdown(
                            id="crossfilter-xaxis-column",
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
                            clickData={"points": [{"customdata": [0]}]},
                            hoverData={"points": [{"customdata": [0]}]},
                            # hoverData={
                            #     "points": [
                            #         {
                            #             "customdata": "Hollis & Hollis Group Inc (Clarksville, TN)"
                            #         }
                            #     ]
                            # },
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
                html.H2("Example 5.  Parallel Categories Diagram"),
                html.P(
                    "The parallel categories diagram (also known as parallel sets or alluvial diagram) is a visualization of multi-dimensional categorical data sets. Each variable in the data set is represented by a column of rectangles, where each rectangle corresponds to a discrete value taken on by that variable. The relative heights of the rectangles reflect the relative frequency of occurrence of the corresponding value."
                ),
                html.P(
                    "Combinations of category rectangles across dimensions are connected by ribbons, where the height of the ribbon corresponds to the relative frequency of occurrence of the combination of categories in the data set."
                ),
                html.P(
                    "Use the drop down filters to tailor your analysis based on product category, product, and company."
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
        insertDropDownMenus("parallel-categories"),
        html.Div(
            [dcc.Graph(id="parallel-categories-plot")],
            className="w3-container w3-margin",
        ),
        html.Div(
            [
                html.H2("Example 6.  Dataset Mapping"),
                html.P(
                    "The map view shows the location of companies and their products as circles."
                ),
                html.P(
                    "Use the drop down filters to tailor your analysis based on product category, product, and company."
                ),
                html.P(
                    "The color of circle corresponds to the product type.  The size of the circle corresponds to the product age."
                ),
                html.P("Values are displayed by hovering over the circles."),
            ],
            className="w3-container",
        ),
        insertDropDownMenus("map"),
        html.Div(
            [dcc.Graph(id="map-plot")],
            className="w3-container w3-margin",
        ),
    ]
)
