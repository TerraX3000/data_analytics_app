import pandas as pd
from dash.dependencies import Input
from dash.dependencies import Output
import plotly.express as px
import plotly.graph_objects as go
import dash_table
from .layout import df


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
    @app.callback(
        Output("crossfilter-indicator-scatter", "figure"),
        [
            Input("table-product-category", "value"),
            Input("table-product", "value"),
            Input("table-company", "value"),
            Input("crossfilter-xaxis-column", "value"),
            Input("crossfilter-yaxis-column", "value"),
            Input("crossfilter-xaxis-type", "value"),
            Input("crossfilter-yaxis-type", "value"),
            Input("crossfilter-year--slider", "value"),
        ],
    )
    def update_graph(
        productCategory,
        product,
        company,
        xaxis_column_name,
        yaxis_column_name,
        xaxis_type,
        yaxis_type,
        year_value,
    ):
        print("Running update_graph callback")
        dff = getDataFrameFilteredBy(productCategory, product, company)
        dff = dff[dff["dayofyear"] == year_value]

        fig = px.scatter(
            x=dff[dff["Parameter"] == xaxis_column_name]["Value"],
            y=dff[dff["Parameter"] == yaxis_column_name]["Value"],
            hover_name=dff[dff["Parameter"] == yaxis_column_name]["Company"],
        )

        fig.update_traces(
            customdata=dff[dff["Parameter"] == yaxis_column_name]["Company"]
        )

        print("customdata = " + dff[dff["Parameter"] == yaxis_column_name]["Company"])

        fig.update_xaxes(
            title=xaxis_column_name, type="linear" if xaxis_type == "Linear" else "log"
        )

        fig.update_yaxes(
            title=yaxis_column_name, type="linear" if yaxis_type == "Linear" else "log"
        )

        fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )

        return fig

    # Small time-series plots
    def create_time_series(dff, axis_type, title):

        fig = px.scatter(dff, x="Ops Time", y="Value")

        fig.update_traces(mode="lines+markers")

        fig.update_xaxes(showgrid=False)

        fig.update_yaxes(type="linear" if axis_type == "Linear" else "log")

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

    @app.callback(
        Output("x-time-series", "figure"),
        [
            Input("crossfilter-indicator-scatter", "hoverData"),
            Input("crossfilter-xaxis-column", "value"),
            Input("crossfilter-xaxis-type", "value"),
        ],
    )
    def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
        print("Running update_y_timeseries callback")
        for key, value in hoverData.items():
            print(key, value)
        company_name = hoverData["points"][0]["customdata"]
        dff = df[df["Company"] == company_name]
        dff = dff[dff["Parameter"] == xaxis_column_name]
        title = "<b>{}</b><br>{}".format(company_name, xaxis_column_name)
        return create_time_series(dff, axis_type, title)

    @app.callback(
        Output("y-time-series", "figure"),
        [
            Input("crossfilter-indicator-scatter", "hoverData"),
            Input("crossfilter-yaxis-column", "value"),
            Input("crossfilter-yaxis-type", "value"),
        ],
    )
    def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
        print("Running update_x_timeseries callback")
        dff = df[df["Company"] == hoverData["points"][0]["customdata"]]
        dff = dff[dff["Parameter"] == yaxis_column_name]
        return create_time_series(dff, axis_type, yaxis_column_name)

    # Multi-line plot
    @app.callback(
        Output("multi-line-plot", "figure"),
        [
            Input("table-product-category", "value"),
            Input("table-product", "value"),
            Input("table-company", "value"),
            Input("multi-line-plot-variable", "value"),
            Input("sparkline-01-plot", "clickData"),
        ],
    )
    def update_multi_line_plot(productCategory, product, company, variable, sparkline):
        print("Running update_multi_line_plot callback")

        dff = getDataFrameFilteredBy(productCategory, product, company)
        if sparkline != None:
            print("sparkline:", type(sparkline))
            print("sparkline =", sparkline["points"][0]["customdata"][0])
            df_multi_line = dff.loc[
                df["Parameter"] == sparkline["points"][0]["customdata"][0]
            ]
        else:
            df_multi_line = dff.loc[df["Parameter"] == variable]
        multi_line_fig = px.line(
            df_multi_line,
            x="Ops Time",
            y="Value",
            color="Product",
            line_group="Activity Group Id",
            hover_name="Company",
            hover_data=[
                "Activity Group Id",
                "Parameter",
                "Description",
                "VIN",
                "Product Category",
                "Date",
            ],
        )

        multi_line_fig.update_xaxes(title="Ops Time", type="linear")

        multi_line_fig.update_yaxes(title=variable, type="linear")

        multi_line_fig.update_layout(
            margin={"l": 40, "b": 40, "t": 10, "r": 0}, hovermode="closest"
        )
        return multi_line_fig

    @app.callback(
        Output("param-01-plot", "figure"),
        Input("multi-line-plot", "clickData"),
    )
    def update_param_01_timeseries(hoverData):
        print("Running update_param_01_timeseries callback")
        for key, value in hoverData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        dff = df[df["Company"] == company]
        dff = dff[dff["Parameter"] == "Fuel Usage"]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        title = "<b>{}</b><br>{}".format(company, "Fuel Usage")
        return create_time_series(dff, "Linear", title)

    @app.callback(
        Output("param-02-plot", "figure"),
        [Input("multi-line-plot", "clickData")],
    )
    def update_param_02_timeseries(hoverData):
        print("Running update_param_02_timeseries callback")
        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        dff = df[df["Company"] == company]
        dff = dff[dff["Parameter"] == "Distance"]
        dff = dff[dff["Activity Group Id"] == activityGroupId]
        return create_time_series(dff, "Linear", "Distance")

    def create_sparkline_plot(activityGroupId, title):
        print("Running create_sparkline_plot()")
        dff = df[df["Activity Group Id"] == activityGroupId]

        fig = px.line(
            dff,
            x="Ops Time",
            y="Value",
            facet_row="Parameter",
            color="Parameter",
            facet_row_spacing=0.1,
            height=100,
            width=200,
            hover_data=[
                "Parameter",
            ],
        )
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

        # hide and lock down axes
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)

        # remove facet/subplot labels
        # fig.update_layout(annotations=[], overwrite=True)
        fig.update_layout(overwrite=True)

        # strip down the rest of the plot
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            margin=dict(t=10, l=10, b=10, r=10),
        )

        return fig

    # Sparkline plots
    # @app.callback(
    #     Output("sparkline-group-plot", "figure"),
    #     Input("multi-line-plot", "hoverData"),
    # )
    # def update_sparkline_group(hoverData):
    #     print("Running sparkline-group callback")
    #     for key, value in hoverData.items():
    #         print(key, value)
    #     for key, value in value[0].items():
    #         print(key, value)

    #     if "customdata" in hoverData["points"][0]:
    #         activityGroupId = hoverData["points"][0]["customdata"][0]
    #         print("activityGroupId found! " + str(activityGroupId))
    #     else:
    #         activityGroupId = 1
    #     if "hovertext" in hoverData["points"][0]:
    #         company = hoverData["points"][0]["hovertext"]
    #         print("hovertext found! " + company)
    #     else:
    #         company = "Hollis & Hollis Group Inc (Clarksville, TN)"
    #     title = "Sparkline_Group"
    #     print("Running create_sparkline_plot()")
    #     dff = df[df["Activity Group Id"] == activityGroupId]

    #     fig = px.line(
    #         dff,
    #         x="Ops Time",
    #         y="Value",
    #         facet_col="Sensor Category",
    #         # facet_row="Parameter",
    #         color="Parameter",
    #         facet_col_wrap=4,
    #         facet_col_spacing=0.04,
    #         facet_row_spacing=0.1,
    #         height=100,
    #         width=200,
    #         hover_data=[
    #             "Parameter",
    #         ],
    #     )
    #     fig.add_annotation(
    #         x=0,
    #         y=0.95,
    #         xanchor="left",
    #         yanchor="bottom",
    #         xref="paper",
    #         yref="paper",
    #         showarrow=False,
    #         align="left",
    #         bgcolor="rgba(255, 255, 255, 0.5)",
    #         text=title,
    #     )

    #     # hide and lock down axes
    #     fig.update_xaxes(visible=False, fixedrange=True)
    #     fig.update_yaxes(visible=False, fixedrange=True)

    #     # remove facet/subplot labels
    #     # fig.update_layout(annotations=[], overwrite=True)
    #     # fig.update_layout(overwrite=True)

    #     # strip down the rest of the plot
    #     fig.update_layout(
    #         showlegend=False,
    #         plot_bgcolor="white",
    #         margin=dict(t=10, l=10, b=10, r=10),
    #     )

    #     return fig

    @app.callback(
        Output("sparkline-01-plot", "figure"),
        Input("multi-line-plot", "hoverData"),
    )
    def update_sparkline_01(hoverData):
        print("Running sparkline-01 callback")
        for key, value in hoverData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        title = "Sparkline_01"
        return create_sparkline_plot(activityGroupId, title)

    @app.callback(
        Output("sparkline-02-plot", "figure"),
        Input("multi-line-plot", "hoverData"),
    )
    def update_sparkline_02(hoverData):
        print("Running sparkline-02 callback")
        for key, value in hoverData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        title = "Sparkline_02"
        return create_sparkline_plot(activityGroupId, title)

    @app.callback(
        Output("sparkline-03-plot", "figure"),
        Input("multi-line-plot", "hoverData"),
    )
    def update_sparkline_03(hoverData):
        print("Running sparkline-03 callback")
        for key, value in hoverData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        title = "Sparkline_03"
        return create_sparkline_plot(activityGroupId, title)

    @app.callback(
        Output("sparkline-04-plot", "figure"),
        Input("multi-line-plot", "hoverData"),
    )
    def update_sparkline_04(hoverData):
        print("Running sparkline-03 callback")
        for key, value in hoverData.items():
            print(key, value)
        for key, value in value[0].items():
            print(key, value)

        if "customdata" in hoverData["points"][0]:
            activityGroupId = hoverData["points"][0]["customdata"][0]
            print("activityGroupId found! " + str(activityGroupId))
        else:
            activityGroupId = 1
        if "hovertext" in hoverData["points"][0]:
            company = hoverData["points"][0]["hovertext"]
            print("hovertext found! " + company)
        else:
            company = "Hollis & Hollis Group Inc (Clarksville, TN)"
        title = "Sparkline_04"
        return create_sparkline_plot(activityGroupId, title)

    def updateDropDownOptions(productCategory, product, company):
        print("Running updateDropdownOptionsForCompanyProductTable callback")
        dff = getDataFrameFilteredBy(productCategory, product, company)

        product_categories = dff["Product Category"].unique()
        product_categories_plusAll = product_categories.tolist()
        product_categories_plusAll.insert(0, "All")
        product_categories_options = [
            {"label": i, "value": i} for i in product_categories_plusAll
        ]
        print(product_categories_options)

        product = dff["Product"].unique()
        product_plusAll = product.tolist()
        product_plusAll.insert(0, "All")
        product_options = [{"label": i, "value": i} for i in product_plusAll]

        companies = dff["Company"].unique()
        companies_plusAll = companies.tolist()
        companies_plusAll.insert(0, "All")
        companies_options = [{"label": i, "value": i} for i in companies_plusAll]

        return [product_categories_options, product_options, companies_options]

    # Update dropdown menus for Company-product Table
    @app.callback(
        [
            Output("parallel-categories-product-category", "options"),
            Output("parallel-categories-product", "options"),
            Output("parallel-categories-company", "options"),
        ],
        [
            Input("parallel-categories-product-category", "value"),
            Input("parallel-categories-product", "value"),
            Input("parallel-categories-company", "value"),
        ],
    )
    def updateDropdownOptionsForParallelCategoriesPlot(
        productCategory, product, company
    ):
        return updateDropDownOptions(productCategory, product, company)

    # Update dropdown menus for Company-product Table
    @app.callback(
        [
            Output("table-product-category", "options"),
            Output("table-product", "options"),
            Output("table-company", "options"),
        ],
        [
            Input("table-product-category", "value"),
            Input("table-product", "value"),
            Input("table-company", "value"),
        ],
    )
    def updateDropdownOptionsForCompanyProductTable(productCategory, product, company):
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

    @app.callback(
        Output("parallel-categories-plot", "figure"),
        [
            Input("parallel-categories-product-category", "value"),
            Input("parallel-categories-product", "value"),
            Input("parallel-categories-company", "value"),
        ],
    )
    def updateParallelCategoriesPlot(productCategory, product, company):
        dff = getDataFrameFilteredBy(productCategory, product, company)
        dff = dff.drop_duplicates(
            subset=["Company", "Product Category", "Product", "Purchase Type", "Age"]
        )
        # dff = dff.loc[:, ["Company","Product Category", "Product", "Purchase Type", "Age"]]
        fig = px.parallel_categories(
            dff,
            dimensions=["Product Category", "Product", "Purchase Type", "Age"],
            color="Age",
            # color_continuous_scale=px.colors.sequential.Inferno,
            color_continuous_scale=px.colors.sequential.Rainbow,
            title="Product, Purchase Type, and Age Information",
        )
        return fig