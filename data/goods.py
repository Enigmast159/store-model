import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Goods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    photo_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    seller_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    seller = orm.relation('User')
    category_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('category.id'))
    category = orm.relation('Category')
    comments = orm.relation('Comment', back_populates='goods')
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weight = sqlalchemy.Column(sqlalchemy.String, default=0)
    size = sqlalchemy.Column(sqlalchemy.String, default=0)
