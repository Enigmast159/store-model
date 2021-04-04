from . import db_session
from .orders import Order
from datetime import datetime
from flask import abort, jsonify
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('seller_id', required=True, type=int)
parser.add_argument('goods_id', required=True, type=int)
parser.add_argument('publication_date', required=True, type=datetime.date)
parser.add_argument('is_bought', required=True, type=bool)


def abort_if_order_not_found(order_id):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(404, message=f"Order {order_id} not found")


class OrderResource(Resource):
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Order).get(order_id)
        return jsonify({'order': order.to_dict(
            only=(
                'id', 'seller_id', 'goods_id',
                'publication_date', 'is_bought'))})

    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Order).get(order_id)
        session.delete(order)
        session.commit()
        return jsonify({'success': 'OK'})


class OrderListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({'order': [item.to_dict(
            only=(
                'id', 'seller_id', 'goods_id',
                'publication_date', 'is_bought')) for item in orders]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        order = Order(
            title=args['id'],
            content=args['seller_id'],
            user_id=args['goods_id'],
            is_published=args['publication_date'],
            is_private=args['is_bought']
        )
        session.add(order)
        session.commit()
        return jsonify({'success': 'OK'})