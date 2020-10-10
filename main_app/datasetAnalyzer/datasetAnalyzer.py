import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource

# from pandas_profiling import ProfileReport

import io
import re

from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry, createDropDownChoices
from main_app.main.referenceData import getDatasetSqlName


class dataframeHtmlTableComponents:
    def __init__(self, df):
        if df.index.to_list():
            self.index = df.index.to_list()
        else:
            self.index = list(range(0, len(df.columns.values)))
        self.column_names = df.columns.values
        self.row_data = list(df.values.tolist())


def analyzeDataset(dataset_id, datasetDetails):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetSqlName = log.datasetSqlName
    # print("datasetSqlName =", datasetSqlName)
    # sqlStatement = f"SELECT * FROM {datasetSqlName}"
    # print("sqlStatement =", sqlStatement)
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # print(df.shape)
    # print(df.columns)
    datasetDetails["columnChoices"] = createDropDownChoices(df.columns)
    datasetDetails["describeDataset"] = df.describe(include="all")

    datasetDetails["datasetInfo"] = getDatasetInfo(df)
    datasetDetails["datasetInfo_2"] = datasetDetails["datasetInfo"]

    datasetDetails["datasetPreview"] = dataframeHtmlTableComponents(
        pd.concat([df.head(10).round(3), df.tail(10).round(3)])
    )
    # print("saving report")
    # profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)
    # print(profile)
    # profile.to_file("/tmp/dataset_report.json")
    # profile.to_file("your_report.html")
    return datasetDetails


def getDatasetInfo(df):
    # Create a StringIO object to capture output of df.info since df.info returns output to stdout by default
    buf = io.StringIO()
    df.info(buf=buf)
    datasetInfo = buf.getvalue()
    # print("datasetInfo = ", datasetInfo)
    # Create a list of the dataset ino
    datasetInfo = datasetInfo.splitlines()
    # Define the column headings for display in html table
    datasetInfo[3] = ["#", "Column", "Non-Null Count", "Data Type"]
    # Convert each data row into a list of data elements beginning with row 5 through the
    #  third from last row
    count = 5
    for line in datasetInfo[5:-2]:
        # print("line = ", line)
        # data = line.split()
        # Use regex to split line info into list.  See tester at regexr.com/5d9cq
        # findall returns a list containing a tuple as noted here https://docs.python.org/2/library/re.html
        data = re.findall(
            r"([\S]+)[\s]+([\S]+[\s\S]*)[\s]+([\d]+)[\s]+[\S]+[\s]+([\S]*[\s]*)", line
        )
        # Verify that the row has data and convert the tuple into a list
        if len(data) > 0:
            data = list(data[0])
        # Replace the string with the list of elements
        datasetInfo[count] = data
        count = count + 1
    # print("datasetInfo = ", datasetInfo)
    return datasetInfo


def plotColumn(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # prepare some data
    x = df["index"]
    y = df[columnName]

    # create a new plot with a title and axis labels
    p = figure(
        title="Dataset Name: " + datasetName,
        x_axis_label="Index",
        y_axis_label=columnName,
        sizing_mode="fixed",
        plot_width=1100,
        plot_height=400,
    )

    # add a line renderer with legend and line thickness
    p.line(x, y, legend_label=columnName, line_width=2)

    # show the results
    return p


def categoricalPlot(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    df = pd.read_sql_table(datasetSqlName, db.engine)
    vc = df[columnName].value_counts()
    categories = vc.index.to_list()
    # Set the x_range to the list of categories above
    p = figure(
        x_range=categories,
        plot_height=250,
        plot_width=1100,
        title=datasetName + ": " + columnName + " Counts",
    )

    # Categorical values can also be used as coordinates
    values = vc.to_list()

    source = ColumnDataSource(data=dict(categories=categories, values=values))
    p.vbar(
        x="categories",
        top="values",
        width=0.9,
        source=source,
        legend_field="categories",
        line_color="white",
        fill_color=factor_cmap("categories", palette=Spectral6, factors=categories),
    )

    # Set some properties to make the plot look better
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    # p.y_range.end = 9
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    return p