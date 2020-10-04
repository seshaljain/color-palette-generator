from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import SubmitField
from wtforms.validators import InputRequired


class ImageForm(FlaskForm):
    picture = FileField('Upload image', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg']), InputRequired()])
    submit = SubmitField('Submit')
