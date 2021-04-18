from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddComms(FlaskForm):
    name = TextAreaField('Вы можете написать комментарий здесь:', validators=[DataRequired()])
    submit = SubmitField('Оставить комментарий')
