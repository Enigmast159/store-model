from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class AddComms(FlaskForm):
    name = TextAreaField('Вы можете оставить отзыв здесь:', validators=[DataRequired()])
    submit = SubmitField('Оставить отзыв')
