from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    SubmitField,
    StringField,
    SelectField,
    TimeField,
    BooleanField,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class uploadDatasetForm(FlaskForm):
    datasetName = StringField("Dataset Name", validators=[DataRequired()])
    comment = StringField("Comment (Optional)", validators=[Optional()])
    csvDatasetFile = FileField(
        "Dataset File (*.csv format)",
        validators=[FileAllowed(["csv"]), FileRequired()],
    )
    submitUploadDataset = SubmitField("Upload Dataset")