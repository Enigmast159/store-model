from . import db_session
from .goods import Goods
from flask import abort, jsonify
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)


def abort_if_user_not_found(goods_id):
    session = db_session.create_session()
    goods = session.query(Goods).get(goods_id)
    if not goods:
        abort(404, message=f"Goods {goods_id} not found")


class GoodsResource(Resource):
    def get(self, goods_id):
        abort_if_user_not_found(goods_id)
        session = db_session.create_session()
        goods = session.query(Goods).get(goods_id)
        return jsonify({'goods': goods.to_dict(
            only=('id', 'seller_id', 'price', 'name', 'about'))})

    def delete(self, goods_id):
        abort_if_user_not_found(goods_id)
        session = db_session.create_session()
        goods = session.query(Goods).get(goods_id)
        session.delete(goods)
        session.commit()
        return jsonify({'success': 'OK'})


class GoodsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        goods = session.query(Goods).all()
        return jsonify({'goods': [item.to_dict(
            only=('id', 'seller_id', 'price', 'name', 'about')) for item in goods]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        goods = Goods(**args)
        session.add(goods)
        session.commit()
        return jsonify({'success': 'OK'})
