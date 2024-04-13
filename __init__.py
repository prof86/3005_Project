# __init__.py
from . models import db
from flask_login import LoginManager
from flask import Flask
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'UkwZObVBRx'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password@localhost/health_fitness_club'

    db.init_app(app)
    return app
