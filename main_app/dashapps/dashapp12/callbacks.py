import pandas as pd
from dash.dependencies import Input
from dash.dependencies import Output
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_table
from .layout import df
import datetime


def setDropdownMenuCallbackOutputParameters(idPrefix):
    callbackOutputParameters = [
        Output(idPrefix + "-product-category", "options"),
        Output(idPrefix + "-product", "options"),
        Output(idPrefix + "-company", "options"),
    ]
    return callbackOutputParameters


def setDropdownMenuCallbackInputParameters(idPrefix):
    callbackInputParameters = [
        Input(idPrefix + "-product-category", "value"),
        Input(idPrefix + "-product", "value"),
        Input(idPrefix + "-company", "value"),
    ]
    return callbackInputParameters


def getDataFrameFilteredBy(productCategory, product, company):
    print(f"Running getDataFrameFilteredBy({productCategory}, {product}, {company})")
    dff = df
    if productCategory != "All":
        dff = dff[dff["Product Category"] == productCategory]
    if product != "All":
        dff = dff[dff["Product"] == product]
    if company != "All":
        dff = dff[dff["Company"] == company]
    return dff


# Cross-filter plot
def register_callbacks(app):
    # Update the cross-filter x and y column choices based on available choices for the selected product
    @app.callback(
        [
            Output("crossfilter-xaxis-column", "options"),
            Output("crossfilter-yaxis-column", "options"),
        ],
        [
            Input("cross-filter-product-category", "value"),
            Input("cross-filter-product", "value"),
            Input("cross-filter-company", "value"),
        ],
    )
    def updateAvailableParameterOptions(
        productCategory,
        product,
        company,
    ):
        print(
            f"Running updateAvailableParameterOptions({productCategory}, {product}, {company})"
        )
        dff = getDataFrameFilteredBy(productCategory, product, company)
        parameterOptions = dff["Parameter"].unique()
        parameterOptions = [{"label": i, "value": i} for i in parameterOptions]
        print("parameterOptions=", parameterOptions)
        return [parameterOptions, parameterOptions]

    # Update the multi-line plot variable choices based on available choices for the selected product
    def updateAvailableParameterOptionsMultiPlot(
        productCategory,
        product,
        company,
    ):
        print(
            f"Running updateAvailableParameterOptionsMultiPlot({productCategory}, {product}, {company})"
        )
        dff = getDataFrameFilteredBy(productCategory, product, company)
        parameterOptions = dff["Parameter"].unique()
        parameterOptions = [{"label": i, "value": i} for i in parameterOptions]
        print("parameterOptions=", parameterOptions)
        return [parameterOptions, parameterOptions, parameterOptions]

    @app.callback(
        [
            Output("multi-line-plot-variable", "options"),
            Output("multi-line-subplot-1-variable", "options"),
            Output("multi-line-subplot-2-variable", "options"),
        ],
        setDropdownMenuCallbackInputParameters("multi-line"),
    )
    def updateAvailableParameterOptionsMultiPlotVariable(
        productCategory,
        product,
        company,
    ):
        print(
            f"Running updateAvailableParameterOptionsMultiPlotVariable({productCategory}, {product}, {company})"
        )
        return updateAvailableParameterOptionsMultiPlot(
            productCategory, product, company
        )

    # Update cross-filter plot based on input values
    @app.callback(
        Output("crossfilter-indicator-scatter", "figure"),
        [
            Input("cross-filter-product-category", "value"),
            Input("cross-filter-product", "value"),
            Input("cross-filter-company", "value"),
            Input("crossfilter-xaxis-column", "value"),
            Input("crossfilter-yaxis-column", "value"),
            # Input("crossfilter-xaxis-type", "value"),
            # Input("crossfilter-yaxis-type", "value"),
        ],
    )
    def update_graph(
        productCategory,
        product,
        company,
        xaxis_column_name,
        yaxis_column_name,
        # xaxis_type,
        # yaxis_type,
    ):
        print("Running update_graph callback")
        dff = getDataFrameFilteredBy(productCategory, product, company)
        dff = dff.sort_values(["dayofyear", "Ops Time"])

        # Construct new dataframe ndf with the x-axis-column and y-axis-column as dataframe columns
        ndf = (
            dff[dff["Parameter"] == xaxis_column_name]
            .reset_index()
            .rename(columns={"Value": xaxis_column_name})
        )
        s1 = dff[dff["Parameter"] == yaxis_column_name]["Value"]
        ds1 = (
            s1.to_frame()
            .reset_index()
            .drop(columns=["index"])
            .rename(columns={"Value": yaxis_column_name})
        )
        ndf = pd.concat([ndf, ds1], axis=1)
        fig = px.scatter(
            ndf,
            x=xaxis_column_name,
            y=yaxis_column_name,
            animation_frame="dayofyear",
            # render_mode="webgl",
            labels={"dayofyear": "Julian Day Number"},
            color="Product",
            hover_name="Company",
            hover_data=[
                "Activity Group Id",
                "Ops Time",
                "Product Category",
                "Product",
                "VIN",
                "Date",
            ],
        )

        # fig.update_xaxes(
        #     title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
        # )

        # fig.update_yaxes(
        #     title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
        # )

        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )

        fig["layout"].pop("updatemenus")  # optional, drop animation buttons

        return fig

    # Small time-series plots
    def create_time_series(dff, title):

        fig = px.scatter(dff, x="Ops Time", y="Value")

        fig.update_traces(mode="lines+markers")

        fig.update_xaxes(showgrid=False)

        # fig.update_yaxes(type="linear" if axis_type == "Linear" else "log")

        fig.add_annotation(
            x=0,
            y=0.85,
            xanchor="left",
            yanchor="bottom",
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            bgcolor="rgba(255, 255, 255, 0.5)",
            text=title,
        )

        fig.update_layout(height=225, margin={"l": 20, "b": 30, "r": 10, "t": 10})

        return fig

    # Update the x-time series plot for the cross-filter plot
    @app.callback(
        Output("x-time-series", "figure"),
        [
            Input("crossfilter-indicator-scatter", "clickData"),
            Input("crossfilter-xaxis-column", "value"),
            # Input("crossfilter-xaxis-type", "value"),
        ],
    )
    def update_x_timeseries(clickData, xaxis_column_name):
        print("Running update_y_timeseries callback")
        productCategory = "All"
        product = "All"
        company = "All"
        dff = getDataFrameFilteredBy(productCategory, product, company)
        for key, value in clickData.items():
            print(key, value)
        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 2
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        dff = dff[dff["Parameter"] == xaxis_column_name]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        title = "<b>{}</b><br>{}".format(company, xaxis_column_name)
        return create_time_series(dff, title)

    # Update the y-time series plot for the cross-filter plot
    @app.callback(
        Output("y-time-series", "figure"),
        [
            Input("crossfilter-indicator-scatter", "clickData"),
            Input("crossfilter-yaxis-column", "value"),
            # Input("crossfilter-yaxis-type", "value"),
        ],
    )
    def update_y_timeseries(clickData, yaxis_column_name):
        print("Running update_x_timeseries callback")
        productCategory = "All"
        product = "All"
        company = "All"
        dff = getDataFrameFilteredBy(productCategory, product, company)
        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 2
        dff = dff[dff["Parameter"] == yaxis_column_name]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        return create_time_series(dff, yaxis_column_name)

    # Multi-line plot
    @app.callback(
        Output("multi-line-plot", "figure"),
        [
            Input("multi-line-product-category", "value"),
            Input("multi-line-product", "value"),
            Input("multi-line-company", "value"),
            Input("multi-line-plot-variable", "value"),
        ],
    )
    def update_multi_line_plot(productCategory, product, company, variable):
        print("Running update_multi_line_plot callback")

        dff = getDataFrameFilteredBy(productCategory, product, company)
        df_multi_line = dff.loc[df["Parameter"] == variable]

        # Determine scaling for plot axes
        min_y = df_multi_line["Value"].min()
        max_y = df_multi_line["Value"].max()
        min_y = min_y * 0.2
        max_y = max_y * 1.2

        multi_line_fig = px.line(
            df_multi_line,
            x="Ops Time",
            y="Value",
            range_y=[min_y, max_y],
            color="Product",
            line_group="Activity Group Id",
            render_mode="webgl",
            hover_name="Company",
            hover_data=[
                "Activity Group Id",
                "Parameter",
                "Description",
                "VIN",
                "Product Category",
                "Product",
                "Date",
            ],
        )

        multi_line_fig.update_xaxes(title="Ops Time", type="linear")

        multi_line_fig.update_yaxes(title=variable, type="linear")

        multi_line_fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )
        return multi_line_fig

    # Update the param-01 time-series plot for the multi-line plot
    @app.callback(
        Output("param-01-plot", "figure"),
        [
            Input("multi-line-plot", "clickData"),
            Input("multi-line-subplot-1-variable", "value"),
        ],
    )
    def update_param_01_timeseries(clickData, variable):
        print("Running update_param_01_timeseries callback")
        for key, value in clickData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 2
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        dff = df[df["Company"] == company]
        dff = dff[dff["Parameter"] == variable]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        title = "<b>{}</b><br>{}".format(company, variable)
        return create_time_series(dff, title)

    # Update the param-02 time-series plot for the multi-line plot
    @app.callback(
        Output("param-02-plot", "figure"),
        [
            Input("multi-line-plot", "clickData"),
            Input("multi-line-subplot-2-variable", "value"),
        ],
    )
    def update_param_02_timeseries(clickData, variable):
        print("Running update_param_02_timeseries callback")
        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 2
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        dff = df[df["Company"] == company]
        dff = dff[dff["Parameter"] == variable]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        return create_time_series(dff, variable)

    def create_sparkline_plot(activityGroupId, sensorCategory, title):
        print("Running create_sparkline_plot() for", sensorCategory)
        dff = df[df["Activity Group Id"] == activityGroupId]
        dff = dff[dff["Sensor Category"] == sensorCategory]

        # Create a blank figure and hide the graph if the sensor category is not in the dataframe
        if len(dff) == 0:
            className = "w3-cell w3-hide"
            print("No data found. Setting className=" + className)
            nodataDf = pd.DataFrame(
                {
                    "Ops Time": [0],
                    "Value": [0],
                    "Parameter": ["NA"],
                }
            )
            fig = px.line(nodataDf, x="Ops Time", y="Value", color="Parameter")
            return fig, className
        else:
            className = "w3-cell"
            print("Data found. Setting className=" + className)

        fig = px.line(
            dff,
            x="Ops Time",
            y="Value",
            facet_row="Parameter",
            color="Parameter",
            labels={"Parameter": ""},
            facet_row_spacing=0.05,
            height=110,
            width=300,
            hover_data=[
                "Parameter",
            ],
        )

        # hide and lock down axes
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)

        # remove facet/subplot labels
        fig.update_layout(annotations=[], overwrite=True)

        # Add sparkline title
        fig.add_annotation(
            x=0,
            y=0.95,
            xanchor="left",
            yanchor="bottom",
            xref="paper",
            yref="paper",
            showarrow=False,
            align="left",
            bgcolor="rgba(255, 255, 255, 0.5)",
            text=title,
        )

        # strip down the rest of the plot
        fig.update_layout(
            showlegend=True,  # Include legend for easy identification of parameters
            plot_bgcolor="white",
            margin=dict(t=10, l=10, b=10, r=10),
        )

        fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.99))

        return fig, className

    # Create sparkline title for sparkline plots
    @app.callback(
        Output("sparkline-selection-title", "children"),
        Input("multi-line-plot", "clickData"),
    )
    def update_SparklineTitle(clickData):
        print("Running update_SparklineTitle() callback")
        if "customdata" in clickData["points"][0]:
            print("Sparkline:")
            for key, value in clickData.items():
                print(key, value)
            activityGroupId = clickData["points"][0]["customdata"][0]
            if len(clickData["points"][0]["customdata"]) > 3:
                vin = clickData["points"][0]["customdata"][3]
                productCategory = clickData["points"][0]["customdata"][4]
                product = clickData["points"][0]["customdata"][5]
                date = clickData["points"][0]["customdata"][6]
                date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
                if "hovertext" in clickData["points"][0]:
                    company = clickData["points"][0]["hovertext"]
                    print("hovertext found! " + company)
                else:
                    company = ""
                title = f"**Product Category:** {productCategory} **Product:** {product} **VIN:** {vin} **Activity Group Id:** {activityGroupId} **Date:** {date:%Y-%m-%d} **Company:** {company}"
            else:
                title = f"**Activity Group Id:** {activityGroupId}"
        else:
            activityGroupId = 1
            title = f"**Activity Group Id:** {activityGroupId}"
        # if "hovertext" in clickData["points"][0]:
        #     company = clickData["points"][0]["hovertext"]
        #     print("hovertext found! " + company)
        #     company=""
        # else:
        #     company = "Hollis & Hollis Group Inc (Clarksville, TN)"

        return title

    # Create sparkline plots
    @app.callback(
        [
            Output("sparkline-01-plot", "figure"),
            Output("sparkline-01-plot", "className"),
        ],
        Input("multi-line-plot", "clickData"),
    )
    def update_sparkline_01(clickData):
        print("Running sparkline-01 callback")
        for key, value in clickData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        sensorCategory = "Engine"
        title = "Engine"
        return create_sparkline_plot(activityGroupId, sensorCategory, title)

    @app.callback(
        [
            Output("sparkline-02-plot", "figure"),
            Output("sparkline-02-plot", "className"),
        ],
        Input("multi-line-plot", "clickData"),
    )
    def update_sparkline_02(clickData):
        print("Running sparkline-02 callback")
        for key, value in clickData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        sensorCategory = "GPS"
        title = "GPS"
        return create_sparkline_plot(activityGroupId, sensorCategory, title)

    @app.callback(
        [
            Output("sparkline-03-plot", "figure"),
            Output("sparkline-03-plot", "className"),
        ],
        Input("multi-line-plot", "clickData"),
    )
    def update_sparkline_03(clickData):
        print("Running sparkline-03 callback")
        for key, value in clickData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        sensorCategory = "Screed"
        title = "Screed"
        return create_sparkline_plot(activityGroupId, sensorCategory, title)

    @app.callback(
        [
            Output("sparkline-04-plot", "figure"),
            Output("sparkline-04-plot", "className"),
        ],
        Input("multi-line-plot", "clickData"),
    )
    def update_sparkline_04(clickData):
        print("Running sparkline-04 callback")
        for key, value in clickData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in clickData["points"][0]:
            activityGroupId = clickData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in clickData["points"][0]:
            company = clickData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Standard Construction Company (Whiteville, TN)"
        sensorCategory = "Grade"
        title = "Grade"
        return create_sparkline_plot(activityGroupId, sensorCategory, title)

    # Dynamically update the dropdown choices based on the other dropdown selections
    def updateDropDownOptions(productCategory, product, company):
        print("Running updateDropDownOptions()")
        dff = getDataFrameFilteredBy(productCategory, product, company)

        # Use df to include all product categories in the drop down list
        product_categories = df["Product Category"].unique()
        product_categories_plusAll = product_categories.tolist()
        product_categories_plusAll.insert(0, "All")
        product_categories_options = [
            {"label": i, "value": i} for i in product_categories_plusAll
        ]
        print(product_categories_options)

        # Use dff to only list products that are available for the selected product category
        # or selected company
        product = dff["Product"].unique()
        product_plusAll = product.tolist()
        product_plusAll.insert(0, "All")
        product_options = [{"label": i, "value": i} for i in product_plusAll]

        # Use dff to only list companies that have the selected product category
        # or selected product
        companies = dff["Company"].unique()
        companies_plusAll = companies.tolist()
        companies_plusAll.insert(0, "All")
        companies_options = [{"label": i, "value": i} for i in companies_plusAll]

        return [product_categories_options, product_options, companies_options]

    # Update dropdown menus for Company-product Table
    @app.callback(
        setDropdownMenuCallbackOutputParameters("parallel-categories"),
        setDropdownMenuCallbackInputParameters("parallel-categories"),
    )
    def updateDropdownOptionsForParallelCategoriesPlot(
        productCategory, product, company
    ):
        return updateDropDownOptions(productCategory, product, company)

    # Update dropdown menus for Company-product Table
    @app.callback(
        setDropdownMenuCallbackOutputParameters("table"),
        setDropdownMenuCallbackInputParameters("table"),
    )
    def updateDropdownOptionsForCompanyProductTable(productCategory, product, company):
        return updateDropDownOptions(productCategory, product, company)

    # Update dropdown menus for map
    @app.callback(
        setDropdownMenuCallbackOutputParameters("map"),
        setDropdownMenuCallbackInputParameters("map"),
    )
    def updateDropdownOptionsForMapPlot(productCategory, product, company):
        return updateDropDownOptions(productCategory, product, company)

    @app.callback(
        setDropdownMenuCallbackOutputParameters("multi-line"),
        setDropdownMenuCallbackInputParameters("multi-line"),
    )
    def updateDropdownOptionsForMultiLinePlot(productCategory, product, company):
        return updateDropDownOptions(productCategory, product, company)

    @app.callback(
        setDropdownMenuCallbackOutputParameters("cross-filter"),
        setDropdownMenuCallbackInputParameters("cross-filter"),
    )
    def updateDropdownOptionsForCrossFilterPlot(productCategory, product, company):
        return updateDropDownOptions(productCategory, product, company)

    # Company-Product Table
    @app.callback(
        Output("company-product-table", "figure"),
        [
            Input("table-product-category", "value"),
            Input("table-product", "value"),
            Input("table-company", "value"),
        ],
    )
    def updateTable(productCategory, product, company):
        print("Running updateTable callback")
        dff = df.drop_duplicates(
            subset=["Company", "Product Category", "Product", "VIN"]
        )
        dff = dff[["Company", "Product Category", "Product", "VIN"]]
        if productCategory != "All":
            dff = dff[dff["Product Category"] == productCategory]
        if product != "All":
            dff = dff[dff["Product"] == product]
        if company != "All":
            dff = dff[dff["Company"] == company]
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=[
                            "Company",
                            "Product Category",
                            "Product",
                            "VIN",
                        ],
                        font=dict(size=10),
                        align="left",
                    ),
                    cells=dict(
                        values=[dff[k].tolist() for k in dff.columns[0:]],
                        align="left",
                    ),
                )
            ],
        )

        return fig

    # Update the data table
    @app.callback(
        [Output("table", "columns"), Output("table", "data")],
        [
            Input("table-product-category", "value"),
            Input("table-product", "value"),
            Input("table-company", "value"),
        ],
    )
    def updateDashTable(productCategory, product, company):
        print("Running updateDashTable callback")
        dff = df.drop_duplicates(
            subset=["Company", "Product Category", "Product", "VIN"]
        )
        dff = dff[["Company", "Product Category", "Product", "VIN"]]
        if productCategory != "All":
            dff = dff[dff["Product Category"] == productCategory]
        if product != "All":
            dff = dff[dff["Product"] == product]
        if company != "All":
            dff = dff[dff["Company"] == company]
        columns = [{"name": i, "id": i} for i in dff.columns]
        data = dff.to_dict("records")
        return [columns, data]

    # Update the parallel categories plot based on the dropdown selections
    @app.callback(
        Output("parallel-categories-plot", "figure"),
        [
            Input("parallel-categories-product-category", "value"),
            Input("parallel-categories-product", "value"),
            Input("parallel-categories-company", "value"),
        ],
    )
    def updateParallelCategoriesPlot(productCategory, product, company):
        print("Running updateParallelCategoriesPlot callback")
        dff = getDataFrameFilteredBy(productCategory, product, company)
        dff = dff.drop_duplicates(
            subset=["Company", "Product Category", "Product", "Purchase Type", "Age"]
        )
        fig = px.parallel_categories(
            dff,
            dimensions=["Product Category", "Product", "Purchase Type", "Age"],
            color="Age",
            color_continuous_scale=px.colors.sequential.Rainbow,
            title="Product, Purchase Type, and Age Information",
        )
        return fig

    # Create map plot
    @app.callback(
        Output("map-plot", "figure"),
        [
            Input("map-product-category", "value"),
            Input("map-product", "value"),
            Input("map-company", "value"),
        ],
    )
    def updateMapPlot(productCategory, product, company):
        print("Running updateMapPlot callback")
        dff = getDataFrameFilteredBy(productCategory, product, company)
        dff = dff.drop_duplicates(
            subset=[
                "Company",
                "Product Category",
                "Product",
                "Purchase Type",
                "Age",
            ]
        )
        # px.set_mapbox_access_token()
        fig = px.scatter_mapbox(
            dff,
            lat="Latitude",
            lon="Longitude",
            hover_name="Company",
            hover_data=[
                "Product Category",
                "Product",
                "VIN",
            ],
            color="Product",
            size="Age",
            color_continuous_scale=px.colors.sequential.Rainbow,
            size_max=15,
            zoom=6,
            mapbox_style="open-street-map",
        )
        return fig