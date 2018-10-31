from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from flaskblog.models import User

class UploadImageForm(FlaskForm):
    picture = FileField('Upload Image', validators=[FileAllowed(['jpg','png']), DataRequired()])
    submit = SubmitField('Upload')
