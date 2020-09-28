import pandas as pd

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

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


def drop_table(table_name):
    engine = db.engine
    base = declarative_base()
    metadata = MetaData(engine, reflect=True)
    table = metadata.tables.get(table_name)
    if table is not None:
        print(f"Deleting {table_name} table")
        base.metadata.drop_all(engine, [table], checkfirst=True)
    return
