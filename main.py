from flask import Flask, render_template, redirect, request, abort
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
run_with_ngrok(app)


@app.route('/')
def index():
    return render_template('base.html', title='Shop on the coach')


def main():
    app.run()


if __name__ == '__main__':
    main()