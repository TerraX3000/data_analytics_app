from main_app import db
from datetime import datetime


class DatasetManager(db.Model):
    __tablename__ = "DatasetManager"
    id = db.Column(db.Integer, primary_key=True)
    datasetName = db.Column(db.String(255), unique=True, nullable=False)
    datasetSqlName = db.Column(db.String(255), unique=True, nullable=False)
    comment = db.Column(db.String(255), nullable=True)
    createDateTime = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)


class ResearchInfo(db.Model):
    __tablename__ = "ResearchInfo"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    weblink = db.Column(db.String(500))
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(500))
    createDateTime = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)