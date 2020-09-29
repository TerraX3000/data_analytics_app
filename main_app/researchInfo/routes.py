from flask import render_template, redirect, url_for, flash, request, Blueprint
from main_app import db
from main_app.models import ResearchInfo
from main_app.researchInfo.forms import addResearchInfoForm, updateResourceForm
from main_app.datasetManager.datasetManager import uploadDataset
from main_app.main.utilityfunctions import printLogEntry, printFormErrors, save_File

researchInfo_bp = Blueprint("researchInfo_bp", __name__)


@researchInfo_bp.route("/researchinfo", methods=["GET", "POST"])
def display_researchInfo():
    addResearchInfoFormDetails = addResearchInfoForm()

    researchInfoLogs = ResearchInfo.query.order_by(
        ResearchInfo.createDateTime.desc()
    ).all()

    if "submitResearchInfo" in request.form:
        if addResearchInfoFormDetails.validate_on_submit():
            printLogEntry("New Research Info Form Submitted")
            title = addResearchInfoFormDetails.title.data
            weblink = addResearchInfoFormDetails.weblink.data
            description = addResearchInfoFormDetails.description.data
            newResearchInfo = ResearchInfo(
                title=title, weblink=weblink, description=description
            )
            db.session.add(newResearchInfo)
            db.session.commit()
            flash("New resource has been added!", "success")
            return redirect(url_for("researchInfo_bp.display_researchInfo"))

    printFormErrors(addResearchInfoFormDetails)

    return render_template(
        "researchinfo.html",
        title="Research Info",
        addResearchInfoForm=addResearchInfoFormDetails,
        researchInfoLogs=researchInfoLogs,
    )


@researchInfo_bp.route("/researchinfo/<int:log_id>/delete", methods=["POST"])
def delete_Resource(log_id):

    log = ResearchInfo.query.get_or_404(log_id)
    LogDetails = f"{(log_id)} {log.title}"
    printLogEntry("Running delete_Resource(" + LogDetails + ")")
    db.session.delete(log)
    db.session.commit()
    flash("Resource has been deleted!", "success")
    return redirect(url_for("researchInfo_bp.display_researchInfo"))


@researchInfo_bp.route(
    "/researchinfo/<int:researchInfo_id>/update", methods=["GET", "POST"]
)
def update_Resource(researchInfo_id):
    printLogEntry("Running update_Resource()")
    resource = ResearchInfo.query.get_or_404(researchInfo_id)
    updateResourceFormDetails = updateResourceForm()
    if "submitUpdatedResource" in request.form:
        if updateResourceFormDetails.validate_on_submit():
            resource.title = updateResourceFormDetails.title.data
            resource.weblink = updateResourceFormDetails.weblink.data
            resource.description = updateResourceFormDetails.description.data
            db.session.commit()
            printLogEntry("Resource info updated for " + resource.title)
            flash("Resource info for " + resource.title + " updated!", "success")
            return redirect(url_for("researchInfo_bp.display_researchInfo"))
    if resource:
        updateResourceFormDetails.researchInfo_id.data = resource.id
        updateResourceFormDetails.title.data = resource.title
        updateResourceFormDetails.weblink.data = resource.weblink
        updateResourceFormDetails.description.data = resource.description
    return render_template(
        "researchinfo_edit.html",
        title="Edit Resource Info",
        updateResourceForm=updateResourceFormDetails,
    )