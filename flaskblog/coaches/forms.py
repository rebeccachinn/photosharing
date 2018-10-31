from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_login import current_user
from flaskblog.models import User


class RateImageForm(FlaskForm):
    rating = IntegerField('Rating', validators=[NumberRange(0,5)])
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')