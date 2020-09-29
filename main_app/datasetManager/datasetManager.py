import pandas as pd

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry


def uploadDataset(datasetName, csvFile, comment):
    printLogEntry("Running uploadDataset()")
    df = pd.read_csv(csvFile)
    datasetSqlName = "dataset_" + str.replace(datasetName, " ", "_")
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


def getRowsAndColumns(dataset_id):
    dataset = DatasetManager.query.get_or_404(dataset_id)
    datasetSqlName = dataset.datasetSqlName
    # sqlStatement = f"SELECT * FROM {datasetSqlName}"
    # df = pd.read_sql_query(sqlStatement, db.engine)
    df = pd.read_sql_table(datasetSqlName, db.engine)
    # print(df.shape)
    rowsAndColumns = str(df.shape[0]) + " x " + str(df.shape[1])
    return rowsAndColumns