from flask import render_template, redirect, url_for, flash, request, Blueprint

import json
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import gridplot, layout, Spacer

import pandas as pd

from main_app import db
from main_app.models import DatasetManager
from main_app.datasetAnalyzer.forms import (
    selectDatasetToAnalyzeForm,
    selectColumnToAnalyzeForm,
)
from main_app.datasetAnalyzer.datasetAnalyzer import (
    dataframeHtmlTableComponents,
    analyzeDataset,
    plotColumn,
    categoricalPlot,
)
from main_app.main.referenceData import getDatasetNames, getWebContent
from main_app.main.utilityfunctions import printLogEntry, printFormErrors, save_File

datasetAnalyzer_bp = Blueprint("datasetAnalyzer_bp", __name__)


@datasetAnalyzer_bp.route("/datasetanalyzer", methods=["GET", "POST"])
def display_datasetAnalyzer():
    selectDatasetToAnalzerFormDetails = selectDatasetToAnalyzeForm()
    selectDatasetToAnalzerFormDetails.datasetName.choices = getDatasetNames()
    selectColumnToAnalyzeFormDetails = selectColumnToAnalyzeForm()
    datasetDetails = {}
    df = pd.DataFrame()
    dfHtmlTableComponents = dataframeHtmlTableComponents(df)
    df_preview_HtmlTableComponents = dataframeHtmlTableComponents(df)
    datasets = DatasetManager.query.all()
    webContent = getWebContent()

    if "submitDatasetToAnalyze" in request.form:
        if selectDatasetToAnalzerFormDetails.validate_on_submit():
            printLogEntry("Dataset to Analyze Form Submitted")
            dataset_id = selectDatasetToAnalzerFormDetails.datasetName.data
            datasetDetails = {}
            datasetDetails = analyzeDataset(dataset_id, datasetDetails)
            # print(datasetDetails)
            # print(datasetDetails["describeDataset"])
            df = datasetDetails["describeDataset"].round(1)
            dfHtmlTableComponents = dataframeHtmlTableComponents(df)
            if datasetDetails["columnChoices"]:
                selectColumnToAnalyzeFormDetails.columnName.choices = datasetDetails[
                    "columnChoices"
                ]
                flash("Dataset Summary Statistics Completed", "success")
            else:
                flash("No columns found in dataset. Check dataset for errors.", "error")
        printFormErrors(selectDatasetToAnalzerFormDetails)

    if "submitColumnToAnalyze" in request.form:
        if selectColumnToAnalyzeFormDetails.validate_on_submit():
            printLogEntry("Column to Analyze Form Submitted")
            columnName = selectColumnToAnalyzeFormDetails.columnName.data
        print(request.form)
        printFormErrors(selectColumnToAnalyzeFormDetails)
        flash("New plot created!", "success")

    return render_template(
        "datasetanalyzer.html",
        title="Dataset Analyzer",
        selectDatasetToAnalyzeForm=selectDatasetToAnalzerFormDetails,
        selectColumnToAnalyzeForm=selectColumnToAnalyzeFormDetails,
        resources=CDN.render(),
        datasetDetails=datasetDetails,
        dfHtmlTableComponents=dfHtmlTableComponents,
        webContent=webContent,
    )


@datasetAnalyzer_bp.route("/plotdatasetcolumn")
def plotDatasetColumn():
    return render_template(
        "datavisualizationsamples.html",
        resources=CDN.render(),
        title="Data Visualization Samples",
    )


@datasetAnalyzer_bp.route("/dataplot/<int:dataset_id>&<columnName>")
def showDataPlot(dataset_id, columnName):
    # Create plot based on dataset and column name
    p = plotColumn(dataset_id, columnName)
    return json.dumps(json_item(p))


@datasetAnalyzer_bp.route("/categoricalplot/<int:dataset_id>&<columnName>")
def showCatergoricalPlot(dataset_id, columnName):
    # Create plot
    p = categoricalPlot(dataset_id, columnName)
    return json.dumps(json_item(p))