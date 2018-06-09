import json
import unittest

from app import create_app, create_db, create_resources
from main import create_tables
from resources.models import User


class ApiTest(unittest.TestCase):

    def setUp(self):
        app = create_app("settings.TestingConfig")
        self.db = create_db(app)
        create_resources(app)
        self.app = app.test_client()
        with app.app_context():
            create_tables()

    def test_get_user(self):
        user = User.create(name='Teste 1')
        data = {'name': 'Teste 1'}
        url = "/users/%s" % user.id
        assert data == self.app.get(url).json

    def test_post_user(self):
        data = {'name': 'Fulano Beltrano'}
        rv = self.app.post('/users', data=json.dumps(data),
                           content_type='application/json').json
        assert data == rv

    def test_update_user(self):
        user = User.create(name='Fulano teste')
        data = {'name': 'Teste update'}
        url = "/users/%s" % str(user.id)
        rv = self.app.put(url, data=json.dumps(data),
                          content_type='application/json').json
        assert data == rv
        assert User.get(id=user.id).name == data["name"]

    def test_delete_api(self):
        user = User.create(name='Teste update')
        url = "/users/%s" % str(user.id)
        rv = self.app.delete(url,
                             content_type='application/json').status_code
        assert rv == 204

    def test_forecast_post(self):
        user = User.create(name='Teste update')
        data = {'user_id': user.id,
                'address': 'Rua Marshmallow',
                'period': {'period_from': '08:00:00',
                           'period_to': '19:00:00'},
                'days': {
                    'sunday': True,
                    'monday': True,
                    'tuesday': True,
                    'wednesday': True,
                    'thursday': True,
                    'friday': False,
                    'saturday': False},

                'notification': '07:00:00'}
        rv = self.app.post("/forecast", data=json.dumps(data),
                           content_type='application/json').json
        data["id"] = rv["id"]
        assert data == rv

    def test_forecast_get(self):
        user = User.create(name='Teste update')
        data = {'user_id': user.id,
                'address': 'Rua Marshmallow',
                'period': {'period_from': '08:00:00',
                           'period_to': '19:00:00'},
                'days': {
                    'sunday': True,
                    'monday': True,
                    'tuesday': True,
                    'wednesday': True,
                    'thursday': True,
                    'friday': False,
                    'saturday': False},

                'notification': '07:00:00'}
        rv = self.app.post("/forecast", data=json.dumps(data),
                           content_type='application/json').json
        data["id"] = rv["id"]
        url = "users/%s/forecast/%s" % (user.id, rv["id"])
        rv = self.app.get(url,
                          content_type='application/json').json
        assert data == rv

        url = "users/1/forecast/540"
        rv = self.app.get(url,
                          content_type='application/json').json
        assert {"message": "Forecast could not be found"} == rv
