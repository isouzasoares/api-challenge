from flask import Flask
from flask_restful import Api
from flask_peewee.db import Database


def create_db(app):
    db = Database(app)
    return db


def create_resources(app):
    from src.resources.user import UserView, UserAdd
    from src.resources.forecast import ForecastView

    api = Api(app)
    # User
    api.add_resource(UserAdd, '/users')
    api.add_resource(UserView, '/users/<user_id>')
    api.add_resource(ForecastView, '/users/<user_id>/forecast/<forecast_id>')


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    return app

app = create_app("settings.BaseConfig")
db = create_db(app)
create_resources(app)
