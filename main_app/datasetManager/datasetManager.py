import pandas as pd
from flask import flash

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from main_app import db
from main_app.models import DatasetManager
from main_app.main.utilityfunctions import printLogEntry
from zipfile import ZipFile


def uploadDataset(datasetName, csvFile, comment, ziptest):
    printLogEntry("Running uploadDataset()")
    # if the file is a zipped csv file, use ZipFile to open it and select the first zipped file to read with pd
    if ziptest:
        zip_file = ZipFile(csvFile)
        print("zip info:", zip_file.infolist()[0].filename)
        df = pd.read_csv(zip_file.open(zip_file.infolist()[0].filename))
        # See explanation for ZipFile at https://stackoverflow.com/questions/44575251/reading-multiple-files-contained-in-a-zip-file-with-pandas
    # If the file is a CSV file, read it directly with pd
    else:
        df = pd.read_csv(csvFile)
    datasetSqlName = "dataset_" + str.replace(datasetName, " ", "_")
    newDataset = DatasetManager(
        datasetName=datasetName, datasetSqlName=datasetSqlName, comment=comment
    )
    try:
        db.session.add(newDataset)
        db.session.commit()
        df.to_sql(datasetSqlName, db.engine)
        flash("Dataset has been uploaded!", "success")
    except:
        print("Error uploading dataset")
        flash("Error uploading dataset", "error")
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