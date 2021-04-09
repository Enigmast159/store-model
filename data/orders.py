import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    customer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    customer = orm.relation('User')
    goods_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("goods.id"))
    product = orm.relation('Goods')
