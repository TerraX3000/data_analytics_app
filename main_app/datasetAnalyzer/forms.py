from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, StringField, SelectField, HiddenField, RadioField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired
from main_app.main.referenceData import getDatasetNames


class selectDatasetToAnalyzeForm(FlaskForm):
    datasetName = SelectField("Dataset Name", validators=[DataRequired()])
    submitDatasetToAnalyze = SubmitField("Analyze Dataset")


class selectColumnToAnalyzeForm(FlaskForm):
    columnName = SelectField("Column Name", validators=[DataRequired()])
    submitColumnToAnalyze = SubmitField("Visualize Data Column")
    plotType = RadioField(
        "Plot Type",
        validators=[DataRequired()],
        choices=[("Line Graph", "Line Graph"), ("Bar Chart", "Bar Chart")],
        default="Line Graph",
    )
