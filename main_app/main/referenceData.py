from main_app.models import DatasetManager, WebContent
from main_app import db
from sqlalchemy import distinct
from datetime import date, timedelta
from main_app.main.utilityfunctions import printLogEntry


def getDatasetNames():
    datasetNameValueLabelTupleList = db.session.query(
        DatasetManager.id, DatasetManager.datasetName
    ).all()
    datasetNameChoices = list(datasetNameValueLabelTupleList)
    datasetNameChoices.insert(0, (0, ""))
    return tuple(datasetNameChoices)


def getDatasetSqlName(datasetName):
    datasetSqlName = (
        db.session.query(DatasetManager.datasetSqlName)
        .filter(DatasetManager.datasetName == datasetName)
        .all()
    )
    return datasetSqlName
