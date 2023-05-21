import csv
import os
import random
import requests
from statistics import mean

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
    with open("requirements.txt", 'r') as f:
        file_content = f.readlines()
        with app.app_context():
            return render_template('requirements.html', file_content=file_content)


@app.route('/generate-users/')
def return_fake_users():
    # Create a collection of unique Ukrainian names
    first_names = list(set(Provider.first_names))

    # If the file exists - clean the content so that each request is a new list
    if os.path.exists('users.txt'):
        with open('users.txt', 'a') as file:
            file.truncate(0)

    # GET parameter for a number of users
    number = int(request.args.get("count", 100))

    # Generate first name in Ukrainian + email first_name@fake_domain
    for i in range(number):
        fake = Faker()
        first_name = random.choice(first_names)
        email = translit(first_name.lower(), 'uk', reversed=True) + '@' + fake.domain_name()
        write_to_file(first_name, email)

    users_list = read_and_return()
    with app.app_context():
        return render_template('generate_users.html', file_content=users_list)


@app.route('/mean/')
def calculate_average():
    rows = []

    with open('hw.csv') as file_obj:
        # Skips the heading
        heading = next(file_obj)

        reader_obj = csv.reader(file_obj)

        for i in reader_obj:
            rows.append(i)

    indexes = rows_divider(rows, 0)
    heights_inches = rows_divider(rows, 1)
    weights_pounds = rows_divider(rows, 2)

    heights_cm = inches_to_cm(heights_inches)
    weights_kg = pounds_to_kg(weights_pounds)

    average_height = round(mean(heights_cm), 2)
    average_mass = round(mean(weights_kg), 2)

    with app.app_context():
        return render_template('average.html', last_index=indexes[-1], average_height=average_height,
                               average_mass=average_mass)


@app.route('/space/')
def return_astronauts_number():
    r = requests.get(' http://api.open-notify.org/astros.json')
    # Dumb solution
    number_basic = (r.json()["number"])

    # Okay, let's do something and count parameter "people"
    number_counted = (len(r.json()["people"]))

    with app.app_context():
        return render_template('astronauts.html', number_basic=number_basic, number_counted=number_counted)


def inches_to_cm(inches_values):
    cm_values = []

    for value in inches_values:
        cm_values.append(round(float(value) * 2.54, 2))

    return cm_values


def pounds_to_kg(pounds_values):
    kg_values = []

    for value in pounds_values:
        kg_values.append(round(float(value) / 2.205, 2))

    return kg_values


def rows_divider(rows, index_number):
    column = []

    for i in rows:
        if len(i) > 0:
            column.append(i[index_number])

    return column


def write_to_file(*args):
    with open('users.txt', 'a') as f:
        list_to_write = [str(x) for x in [*args]]
        f.write(': '.join(list_to_write))
        f.write('\n')


def read_and_return():
    with open("users.txt", 'r') as f:
        file_content = f.readlines()
        return file_content
