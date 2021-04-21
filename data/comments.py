import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Comment(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    goods_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("goods.id"))
    goods = orm.relation('Goods')
    commentator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    commentator = orm.relation('User')
    message = sqlalchemy.Column(sqlalchemy.String, nullable=True)
