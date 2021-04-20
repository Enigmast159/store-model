from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField


class Sort(FlaskForm):
    category = SelectField('Выберите категорию', validators=[], choices=[])
    price = RadioField('Выберите порядок товаров',
                       choices=[(1, 'По возрастанию цены'), (2, 'По убыванию цены'),
                                (3, 'Без изменений')])
    submit = SubmitField('Показать результаты')