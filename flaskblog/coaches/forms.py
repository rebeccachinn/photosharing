from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from flask_login import current_user
from flaskblog.models import User


class RateImageForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    comment = StringField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')