from flask import Flask, render_template, redirect, request, abort, url_for
from flask_restful import Api
from data.db_session import global_init, create_session
from .data import goods_resource, order_resource, user_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)

api.add_resource(goods_resource.GoodsListResource, '/api/goods')
api.add_resource(
    goods_resource.GoodsResource,
    '/api/good/<int:id>/<int:seller_id>/<int:price>/'
    '<str:name>/<str:about>/<str:class_name>/<int:weught>/<str:size>')

api.add_resource(order_resource.OrderListResource, '/api/orders')
api.add_resource(
    order_resource.OrderResource,
    '/api/order/<int:id>/<int:customer_id>/<int:goods_id>')

api.add_resource(user_resource.UsersListResource, '/api/users')
api.add_resource(
    user_resource.UserResource,
    '/api/user/<int:id>/<str:name>/<str:surname>/<str:email>/'
    '<str:about>/<str:hashed_password>/<str:created_date>/<str:birthdate>')


@app.route('/')
@app.route('/about_us')
def index():
    return render_template('about_us.html', title='Shop on the coach')


def main():
    global_init("db/trading_area.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
