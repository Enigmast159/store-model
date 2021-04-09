from flask import Flask, render_template, redirect, request, abort, url_for
from forms.registration import RegisterForm
from forms.login import LoginForm
from forms.add_goods import AddGoods
from data.db_session import global_init, create_session
from data import db_session
from data.users import User
from data.goods import Goods
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
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


@app.route('/catalog')
@login_required
def catalog():
    return render_template('catalog.html', title='Каталог')


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


def main():
    global_init("db/trading_area.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
