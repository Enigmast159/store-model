# Импорт всех необходимых библиотек и файлов
from flask import Flask, render_template, redirect, request, abort
from forms.registration import RegisterForm
from forms.login import LoginForm
from forms.add_goods import AddGoods
from forms.comm import AddComms
from forms.sort import Sort
from flask_restful import Api
from data.db_session import global_init, create_session
from data import db_session
from data.users import User
from data.comments import Comment
from data.goods import Goods
from data.category import Category
from data.orders import Order
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime
from data import goods_resource, order_resource, user_resource, comments_resource
import os
#import logging
# Логгирование уведомлений в отдельный файл
#logging.basicConfig(level=logging.INFO, filename='example.log',
                    #format='%(asctime)s %(levelname)s %(name)s %(message)s')
app = Flask(__name__)  # Создание приложения
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)  # Создание api
# Добавление ресурсов в api
api.add_resource(goods_resource.GoodsListResource, '/api/goods')
api.add_resource(goods_resource.GoodsResource, '/api/goods/<int:goods_id>')

api.add_resource(order_resource.OrderListResource, '/api/orders')
api.add_resource(order_resource.OrderResource, '/api/orders/<int:order_id>')

api.add_resource(user_resource.UsersListResource, '/api/users')
api.add_resource(user_resource.UserResource, '/api/users/<int:user_id>')

api.add_resource(comments_resource.CommentListResource, '/api/comments')
api.add_resource(comments_resource.CommentResource, '/api/comments/<int:msg_id>')
login_manager = LoginManager()
login_manager.init_app(app)


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


# Главная страница
@app.route('/')
@app.route('/about_us')
def index():
    return render_template('about_us.html', title='Shop on the coach')


# Страница регистрации
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
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


# Страница изменения профиля
@app.route('/edit_user/<int:user_id>', methods=['POST', 'GET'])
@login_required
def edit_user(user_id):
    form = RegisterForm()
    session = db_session.create_session()
    user = session.query(User).filter(User.id == user_id).first()
    if request.method == 'GET':
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.about.data = user.about
            form.email.data = user.email
            form.bdate.data = user.birthdate
        else:
            abort(404)
    if form.validate_on_submit():
        if user:
            user.name = form.name.data
            user.surname = form.surname.data
            user.email = form.email.data
            user.about = form.about.data
            user.birthdate = form.bdate.data
            text = form.photo.data.read()
            if not (str(text) == "b''"):
                name = str(form.photo.data)
                name = name.split('.')[-1].split("'")[0]
                user.photo_id = f'{user.id}.{name}'
                with open(f'static/img/user_img/{user.photo_id}', 'wb') as f:
                    f.write(text)
            session.merge(user)
            session.commit()
            return redirect(f'/user_page/{user_id}')
        else:
            abort(404)
    msg = 'Вы можете редактировать только эти поля: имя, фамилия, почта, дата рождения, фото'
    return render_template('register.html', title='Редактирование профиля', form=form, msg=msg)


# Страница авторизации пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/about_us")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


# Выход пользователя из аккаунта
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


# Каталог товаров
@app.route('/catalog', methods=['POST', 'GET'])
def catalog():
    db_sess = db_session.create_session()
    form = Sort()
    items = db_sess.query(Category).all()
    form.category.choices = [(item.id + 1, item.name) for item in items]
    form.category.choices.append((1, 'Все'))
    form.category.choices = form.category.choices[::-1]
    goods = db_sess.query(Goods).all()
    if form.validate_on_submit():
        print(form.category.data)
        if form.category.data == '1':
            goods = db_sess.query(Goods).all()
        else:
            goods = db_sess.query(Goods).filter(Goods.category_id == int(form.category.data) - 1
                                                ).all()
        if form.price.data == '1':
            goods = sorted(goods, key=lambda x: x.price)
        elif form.price.data == '2':
            goods = sorted(goods, key=lambda x: x.price)[::-1]
        return render_template('catalog.html', title='Каталог', goods=goods, form=form)
    return render_template('catalog.html', title='Каталог', goods=goods, form=form)


# Страница добавления товаров
@app.route('/add_goods', methods=['GET', 'POST'])
@login_required
def add_goods():
    form = AddGoods()
    db_sess = db_session.create_session()
    items = db_sess.query(Category).all()
    form.select.choices = [(item.id, item.name) for item in items]
    if form.validate_on_submit():
        goods = Goods(
            name=form.name.data,
            about=form.about.data,
            price=form.price.data,
            category_id=form.select.data
        )
        current_user.goods.append(goods)
        db_sess.merge(current_user)
        db_sess.commit()
        name = str(form.photo.data)
        name = name.split('.')[-1].split("'")[0]
        text = form.photo.data.read()
        goods = db_sess.query(Goods).all()[-1]
        if str(text) == "b''":
            goods.photo_id = 'pepe.gif'
        else:
            goods.photo_id = f'{goods.id}.{name}'
            with open(f'static/img/goods_img/{goods.photo_id}', 'wb') as f:
                f.write(text)
        db_sess.merge(goods)
        db_sess.commit()
        return redirect('/catalog')
    return render_template('add_goods.html', title='Добавление товара', form=form)


# Удаление товара
@app.route('/delete_goods/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def delete_goods(goods_id):
    db_sess = db_session.create_session()
    goods = db_sess.query(Goods).filter(Goods.id == goods_id).first()
    if goods:
        db_sess.delete(goods)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/catalog')


# Изменение товара
@app.route('/edit_goods/<int:goods_id>', methods=['GET', 'POST'])
@login_required
def edit_goods(goods_id):
    form = AddGoods()
    session = db_session.create_session()
    items = session.query(Category).all()
    form.select.choices = [(item.id, item.name) for item in items]
    goods = session.query(Goods).filter(Goods.id == goods_id, Goods.seller == current_user).first()
    if request.method == 'GET':
        if goods:
            form.name.data = goods.name
            form.about.data = goods.about
            form.price.data = goods.price
            form.weight.data = goods.weight
            form.size.data = goods.size
            form.select.data = goods.category_id
        else:
            abort(404)
    if form.validate_on_submit():
        if goods:
            goods.name = form.name.data
            goods.about = form.about.data
            goods.price = form.price.data
            goods.weight = form.weight.data
            goods.size = form.size.data
            goods.category_id = form.select.data
            session.merge(goods)
            session.commit()
            return redirect('/catalog')
        else:
            abort(404)
    return render_template('add_goods.html', title='Редактирование товара', form=form)


# Страница товара
@app.route('/item_page/<int:goods_id>', methods=['POST', 'GET'])
def item_page(goods_id):
    form = AddComms()
    db_sess = db_session.create_session()
    item = db_sess.query(Goods).get(goods_id)
    comms = db_sess.query(Comment).filter(Comment.goods == item).all()
    if form.validate_on_submit():
        comm = Comment(
            commentator_id=current_user.id,
            message=form.name.data,
            goods_id=item.id
        )
        db_sess.add(comm)
        db_sess.commit()
        comms = db_sess.query(Comment).filter(Comment.goods == item).all()
        return render_template('item_page.html', item=item, title=f'Товар: {item.name}',
                               comments=comms, form=form)
    return render_template('item_page.html', item=item, title=f'Товар: {item.name}',
                           comments=comms, form=form)


# Удаление комментария
@app.route('/comment_delete/<int:comm_id>/<int:g_id>', methods=['POST', 'GET'])
@login_required
def comment_delete(comm_id, g_id):
    db_sess = db_session.create_session()
    comm = db_sess.query(Comment).get(comm_id)
    if comm:
        db_sess.delete(comm)
        db_sess.commit()
    else:
        abort(404)
    return redirect(f'/item_page/{g_id}')


# Страница профиля пользователя
@app.route('/user_page/<int:user_id>')
@login_required
def user_page(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    orders = db_sess.query(Order).filter(Order.customer == user).all()
    arr = []
    for item in orders:
        arr.append(item.goods_id)
    goods = []
    for i in arr:
        goods.append(db_sess.query(Goods).get(i))
    return render_template('user_page.html', item=user,
                           title=f'DuckDuckShop', goods=goods, len=len(arr))


# Оформление заказа
@app.route('/make_order/<int:customer_id>/<int:goods_id>')
@login_required
def make_order(customer_id, goods_id):
    db_sess = db_session.create_session()
    order = Order(
        customer_id=customer_id,
        goods_id=goods_id
    )
    db_sess.add(order)
    db_sess.commit()
    return redirect('/catalog')


# Очищение корзины
@app.route('/fresh_cart')
@login_required
def fresh_cart():
    db_sess = db_session.create_session()
    orders = db_sess.query(Order).filter(Order.customer == current_user).first()
    while orders:
        db_sess.delete(orders)
        orders = db_sess.query(Order).filter(Order.customer == current_user).first()
    db_sess.commit()
    return redirect(f'/user_page/{current_user.id}')


# Запуск
if __name__ == '__main__':
    global_init("db/trading_area.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
