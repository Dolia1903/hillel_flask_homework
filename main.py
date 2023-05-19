from flask import Flask
from flask import send_file

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/requirements/')
def return_requirements_file():
    try:
        return send_file('/home/dolia/hillel_flask_homework/hillel_flask_homework/requirements.txt')
    except Exception as e:
        return str(e)
