from flask import Flask, render_template, redirect, request, abort, url_for
from forms.registration import RegisterForm
from forms.login import LoginForm
from forms.add_goods import AddGoods
from flask_restful import Api
from data.db_session import global_init, create_session
from data import db_session
from data.users import User
from data.goods import Goods
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime
from data import goods_resource, order_resource, user_resource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)

api.add_resource(goods_resource.GoodsListResource, '/api/goods')
api.add_resource(
    goods_resource.GoodsResource,
    '/api/good/<int:id>/<int:seller_id>/<int:price>/' +
    '<string:name>/<string:about>/<string:class_name>/<int:weight>/<string:size>')

api.add_resource(order_resource.OrderListResource, '/api/orders')
api.add_resource(
    order_resource.OrderResource,
    '/api/order/<int:id>/<int:customer_id>/<int:goods_id>')

api.add_resource(user_resource.UsersListResource, '/api/users')
api.add_resource(
    user_resource.UserResource,
    '/api/user/<int:id>/<string:name>/<string:surname>/<string:email>/' +
    '<string:about>/<string:hashed_password>/<string:created_date>/<string:birthdate>')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/about_us')
def index():
    return render_template('about_us.html', title='Shop on the coach')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            created_date=datetime.datetime.now(),
            about=form.about.data,
            birthdate=form.bdate.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/edit_user/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_user(id):
    form = RegisterForm()
    session = db_session.create_session()
    user = session.query(User).get(id)
    if request.method == 'GET':
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.about.data = user.about
            form.bdate.data = user.birthdate
            form.email.data = user.email
            form.password.data = ''
        else:
            abort(404)
    if form.validate_on_submit():
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.about = form.about.data
            user.email = form.email.data
            user.bdate = form.bdate.data
            user.set_password(form.password.data)
            session.merge(user)
            session.commit()
            return redirect(f'/user_page/{id}')
        else:
            abort(404)
    return render_template('register.html', title='Редактирование профиля', form=form)


@app.route('/catalog')
@login_required
def catalog():
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).all()
    return render_template('catalog.html', title='Каталог', goods=goods)


@app.route('/add_goods', methods=['GET', 'POST'])
@login_required
def add_goods():
    form = AddGoods()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        goods = Goods(
            name=form.name.data,
            about=form.about.data,
            weight=form.weight.data,
            size=form.size.data,
            price=form.price.data
        )
        current_user.goods.append(goods)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/catalog')
    return render_template('add_goods.html', title='Добавление товара', form=form)


@app.route('/delete_goods/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_goods(id):
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).filter(Goods.id == id).first()
    if goods:
        db_sess.delete(goods)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/catalog')


@app.route('/edit_goods/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_goods(id):
    form = AddGoods()
    session = db_session.create_session()
    goods = session.query(Goods).filter(Goods.id == id, Goods.seller == current_user).first()
    if request.method == 'GET':
        if goods:
            form.name.data = goods.name
            form.about.data = goods.about
            form.price.data = goods.price
            form.weight.data = goods.weight
            form.size.data = goods.size
        else:
            abort(404)
    if form.validate_on_submit():
        if goods:
            goods.name = form.name.data
            goods.about = form.about.data
            goods.price = form.price.data
            goods.weight = form.weight.data
            goods.size = form.size.data
            session.merge(goods)
            session.commit()
            return redirect('/catalog')
        else:
            abort(404)
    return render_template('add_goods.html', title='Редактирование товара', form=form)


@app.route('/item_page/<int:id>')
@login_required
def item_page(id):
    db_sess = db_session.create_session()
    item = db_sess.query(Goods).get(id)
    return render_template('item_page.html', item=item, title=f'Товар: {item.name}')


@app.route('/user_page/<int:id>')
@login_required
def user_page(id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)
    return render_template('user_page.html', item=user,
                           title=f'Пользователь: {user.name} {user.surname}')


def main():
    global_init("db/trading_area.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
