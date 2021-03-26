from flask import Flask, render_template, redirect, request, abort, url_for
from data.db_session import global_init, create_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'


@app.route('/')
@app.route('/about_us')
def index():
    return render_template('about_us.html', title='Shop on the coach')


def main():
    global_init("db/trading_area.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()
