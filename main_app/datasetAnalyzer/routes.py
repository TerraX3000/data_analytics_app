from flask import render_template, redirect, url_for, flash, request, Blueprint

import json
from bokeh.resources import CDN
from bokeh.embed import json_item
from bokeh.layouts import gridplot, layout, Spacer

from main_app import db
from main_app.models import DatasetManager
from main_app.datasetAnalyzer.forms import (
    selectDatasetToAnalyzeForm,
    selectColumnToAnalyzeForm,
)
from main_app.datasetAnalyzer.datasetAnalyzer import analyzeDataset, plotColumn
from main_app.main.referenceData import getDatasetNames
from main_app.main.utilityfunctions import printLogEntry, printFormErrors, save_File

datasetAnalyzer_bp = Blueprint("datasetAnalyzer_bp", __name__)


@datasetAnalyzer_bp.route("/datasetanalyzer", methods=["GET", "POST"])
def display_datasetAnalyzer():
    selectDatasetToAnalzerFormDetails = selectDatasetToAnalyzeForm()
    selectDatasetToAnalzerFormDetails.datasetName.choices = getDatasetNames()
    selectColumnToAnalyzeFormDetails = selectColumnToAnalyzeForm()

    datasets = DatasetManager.query.all()

    if "submitDatasetToAnalyze" in request.form:
        if selectDatasetToAnalzerFormDetails.validate_on_submit():
            printLogEntry("Dataset to Analyze Form Submitted")
            datasetName = selectDatasetToAnalzerFormDetails.datasetName.data
            columnNames = analyzeDataset(datasetName)
            # print(columnNames)
            selectColumnToAnalyzeFormDetails.columnName.choices = columnNames
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
    # Create plots
    # columnName = "Age"
    p = plotColumn(dataset_id, columnName)
    # Define column and row spacers
    # Spacer: margin - property type: Tuple ( Int , Int , Int , Int )
    # Allows to create additional space around the component.
    # The values in the tuple are ordered as follows - Margin-Top, Margin-Right, Margin-Bottom and Margin-Left

    # Create a grid layout of plots
    return json.dumps(json_item(p))