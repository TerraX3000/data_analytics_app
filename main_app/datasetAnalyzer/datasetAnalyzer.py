import pandas as pd

from bokeh.plotting import figure, output_file, show

from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry, createDropDownChoices
from main_app.main.referenceData import getDatasetSqlName


def analyzeDataset(dataset_id):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetSqlName = log.datasetSqlName
    # print("datasetSqlName =", datasetSqlName)
    # sqlStatement = f"SELECT * FROM {datasetSqlName}"
    # print("sqlStatement =", sqlStatement)
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # print(df.shape)
    # print(df.columns)
    columnChoices = createDropDownChoices(df.columns)
    return columnChoices


def plotColumn(dataset_id, columnName):
    log = DatasetManager.query.get_or_404(dataset_id)
    datasetName = log.datasetName
    datasetSqlName = log.datasetSqlName
    sqlStatement = f"SELECT * FROM {datasetSqlName}"
    df = pd.read_sql_query(sqlStatement, db.engine)
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
