import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    goods_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("goods.id"))
    product = orm.relation('Goods')
    publication_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_bought = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
