from . import db_session
from .users import User
from datetime import datetime
from flask import abort, jsonify
from flask_restful import reqparse, Resource

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True, type=str)
parser.add_argument('surname', required=True, type=str)
parser.add_argument('email', required=True, type=str)
parser.add_argument('about', required=False, type=str)
parser.add_argument('hashed_password', required=False, type=str)
parser.add_argument('created_date', required=False, type=datetime.date)
parser.add_argument('birthdate', required=False, type=datetime.date)


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'about', 'birthdate'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=('id', 'name', 'surname', 'about', 'birthdate')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(**args)
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
