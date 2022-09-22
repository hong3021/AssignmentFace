from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    app.config['SERECT_KEY'] = 'gfhgfh qwevcbccv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .view import views
    # from .GenerateData import GenerateData

    app.register_blueprint(views, url_prefix='/')


    # from website.model import User
    # create_database(app)
    return app


# def create_database(app):
#     if not os.path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('database create!')
