import pandas as pd
from sqlalchemy import create_engine
from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry


def uploadDataset(datasetName, csvFile, comment):
    printLogEntry("Running uploadDataset()")
    df = pd.read_csv(csvFile)
    datasetSqlName = str.replace(datasetName, " ", "_")
    newDataset = DatasetManager(
        datasetName=datasetName, datasetSqlName=datasetSqlName, comment=comment
    )
    try:
        db.session.add(newDataset)
        db.session.commit()
        df.to_sql(datasetSqlName, db.engine)
    except:
        print("Error uploading dataset")

    return