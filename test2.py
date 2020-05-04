import os
from flask import Flask
app = Flask(__name__)


def fun():
    os.system("python test1.py")


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name #Enter http://127.0.0.1:5000/user/joe


if __name__ == '__main__':
    app.run(debug=True)