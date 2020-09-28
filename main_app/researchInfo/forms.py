from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    SubmitField,
    StringField,
    SelectField,
    HiddenField,
    TimeField,
    BooleanField,
    TextAreaField,
    SelectMultipleField,
    widgets,
)
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional


class addResearchInfoForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    weblink = StringField("Weblink", validators=[Optional()])
    description = TextAreaField("Description", render_kw={"rows": "10"})
    submitResearchInfo = SubmitField("Add New Resource")


class updateResourceForm(FlaskForm):
    researchInfo_id = HiddenField()
    title = StringField("Title", validators=[DataRequired()])
    weblink = StringField("Weblink", validators=[Optional()])
    description = TextAreaField("Description", render_kw={"rows": "10"})
    submitUpdatedResource = SubmitField("Update Resource")