import os
import random

from faker import Faker
from faker.providers.person.uk_UA import Provider
from flask import Flask, render_template, request
from flask import send_file
from transliterate import translit

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


@app.route('/generate-users/')
def return_fake_users():
    # Create a collection of unique Ukrainian names
    first_names = list(set(Provider.first_names))

    # If the file exists - clean the content so that each request is a new list
    if os.path.exists('users.txt'):
        with open('users.txt', 'a') as file:
            file.truncate(0)

    # GET parameter for a number of users
    number = int(request.args.get("count"))

    # Generate first name in Ukrainian + email first_name@fake_domain
    for i in range(number):
        fake = Faker()
        first_name = random.choice(first_names)
        email = translit(first_name.lower(), 'uk', reversed=True) + '@' + fake.domain_name()
        write_to_file(first_name, email)

    users_list = read_and_return()
    with app.app_context():
        return render_template('generate_users.html', file_content=users_list)


def write_to_file(*args):
    with open('users.txt', 'a') as f:
        list_to_write = [str(x) for x in [*args]]
        f.write(': '.join(list_to_write))
        f.write('\n')


def read_and_return():
    with open("users.txt", 'r') as f:
        file_content = f.readlines()
        return file_content

