from flask import render_template, redirect, url_for, flash, request, Blueprint
from alembic import op
from main_app import db
from main_app.models import DatasetManager
from main_app.datasetManager.forms import uploadDatasetForm
from main_app.datasetManager.datasetManager import (
    uploadDataset,
    drop_table,
    getRowsAndColumns,
)
from main_app.main.utilityfunctions import printLogEntry, printFormErrors, save_File

datasetManager_bp = Blueprint("datasetManager_bp", __name__)


@datasetManager_bp.route("/datasetmanager", methods=["GET", "POST"])
def display_datasetManager():
    uploadDatasetFormDetails = uploadDatasetForm()

    datasets = DatasetManager.query.all()
    datasetDetails = []
    for dataset in datasets:
        datasetDetails.append(getRowsAndColumns(dataset.id))

    if "submitUploadDataset" in request.form:
        if uploadDatasetFormDetails.validate_on_submit():
            printLogEntry("Upload Dataset Form Submitted")
            if uploadDatasetFormDetails.csvDatasetFile.data:
                uploadedDatasetFile = save_File(
                    uploadDatasetFormDetails.csvDatasetFile.data,
                    "Uploaded_Dataset_File.csv",
                )
                datasetName = uploadDatasetFormDetails.datasetName.data
                comment = uploadDatasetFormDetails.comment.data
                uploadDataset(datasetName, uploadedDatasetFile, comment)

                return redirect(url_for("datasetManager_bp.display_datasetManager"))

    printFormErrors(uploadDatasetFormDetails)

    return render_template(
        "datasetmanager.html",
        title="Dataset Manager",
        uploadDatasetForm=uploadDatasetFormDetails,
        datasets=datasets,
        datasetDetails=datasetDetails,
    )


@datasetManager_bp.route("/datasetmanager/<int:log_id>/delete", methods=["POST"])
def delete_Dataset(log_id):

    log = DatasetManager.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.datasetName}"
    datasetSqlName = log.datasetSqlName
    printLogEntry("Running delete_Dataset(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    drop_table(datasetSqlName)
    flash("Dataset has been deleted!", "success")
    return redirect(url_for("datasetManager_bp.display_datasetManager"))