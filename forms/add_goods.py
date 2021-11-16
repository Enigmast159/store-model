from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired


class AddGoods(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    photo = FileField('Фото', validators=[])
    about = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    select = SelectField('Выберете категорию', validators=[DataRequired()],
                         choices=[])
    submit = SubmitField('Готово')
