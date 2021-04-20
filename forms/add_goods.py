from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired


class AddGoods(FlaskForm):
    name = StringField('Наименование', validators=[DataRequired()])
    photo = FileField('Фото', validators=[])
    about = TextAreaField('Описание', validators=[DataRequired()])
    price = IntegerField('Цена товара', validators=[DataRequired()])
    weight = StringField('Вес товара*', validators=[])
    size = StringField('Размеры товара в формате: ДД х ШШ х ВВ в м*', validators=[])
    select = SelectField('Выберете категорию', validators=[DataRequired()],
                         choices=[])
    submit = SubmitField('Готово')
