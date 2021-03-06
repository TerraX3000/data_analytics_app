import os
from flask import send_file, current_app
from datetime import datetime


def save_File(form_UploadedFileData, filename):
    # file_path = os.path.join(current_app.root_path, "static/upload", filename)
    file_path = "/tmp" + "/" + filename
    form_UploadedFileData.save(file_path)
    return file_path


def download_File(filename):
    # file_path = os.path.join(current_app.root_path, "static/uploadfiles", filename)
    file_path = "/tmp" + "/" + filename
    print("download_File function called with filename=", file_path)
    return send_file(file_path, as_attachment=True, cache_timeout=0)


def printLogEntry(logEntry):
    logtime = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]  ")
    print(logtime, "***", logEntry, "***")
    return


def printFormErrors(form):
    if form.errors:
        printLogEntry("Form errors:" + str(form.errors))
    return


def createDropDownChoices(choiceslist):
    DropDownList = []
    for choice in choiceslist:
        DropDownList.append((choice, choice))
    DropDownChoices = tuple(DropDownList)
    # print(DropDownChoices)
    return DropDownChoices