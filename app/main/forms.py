from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional


class StudySessionForm(FlaskForm):
    """Form for logging a study session on the dashboard."""

    subject_id = SelectField("Subject", coerce=int, validators=[DataRequired()])
    hours = FloatField(
        "Hours Studied",
        validators=[DataRequired(), NumberRange(min=0.25, max=24, message="Enter between 0.25 and 24 hours.")],
    )
    studied_on = DateField(
        "Date",
        validators=[DataRequired()],
        default=date.today,
    )
    notes = TextAreaField("Notes (optional)", validators=[Optional()])
    submit = SubmitField("Log Study Session")
