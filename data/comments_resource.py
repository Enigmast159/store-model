from . import db_session
from .comments import Comment
from flask import abort, jsonify
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('goods_id', required=True, type=int)
parser.add_argument('message', required=True, type=str)


def abort_if_comment_not_found(msg_id):
    session = db_session.create_session()
    msg = session.query(Comment).get(msg_id)
    if not msg:
        abort(404, message=f"Comment {msg_id} not found")


class CommentResource(Resource):
    def get(self, msg_id):
        abort_if_comment_not_found(msg_id)
        session = db_session.create_session()
        msg = session.query(Comment).get(msg_id)
        return jsonify({'comment': msg.to_dict(
            only=('id', 'goods_id', 'message'))})

    def delete(self, msg_id):
        abort_if_comment_not_found(msg_id)
        session = db_session.create_session()
        msg = session.query(Comment).get(msg_id)
        session.delete(msg)
        session.commit()
        return jsonify({'success': 'OK'})


class CommentListResource(Resource):
    def get(self):
        session = db_session.create_session()
        comments = session.query(Comment).all()
        return jsonify({'comment': [item.to_dict(
            only=(
                'id', 'goods_id', 'message')) for item in comments]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        comment = Comment(**args)
        session.add(comment)
        session.commit()
        return jsonify({'success': 'OK'})