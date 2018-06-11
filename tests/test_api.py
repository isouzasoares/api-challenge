import json
import unittest

from app import create_app, create_db, create_resources
from main import create_tables
from resources.models import User, Period, Days, Forecast


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
        forecast_dict = {'address': 'Rua Marshmallow',
                         'notification': '07:00:00'}
        forecast_dict["period"] = {'period_from': '08:00:00',
                                   'period_to': '19:00:00'}
        forecast_dict["days"] = {'sunday': True,
                                 'monday': True,
                                 'tuesday': True,
                                 'wednesday': True,
                                 'thursday': True,
                                 'friday': False,
                                 'saturday': False}
        forecast = Forecast.create(user=user, **forecast_dict)
        Period.create(period=forecast, **forecast_dict["period"])
        Days.create(days=forecast, **forecast_dict["days"])
        data = {'id': user.id, 'name': 'Teste 1', 'forecast': [forecast_dict]}
        url = "/users/%s" % user.id
        assert data == self.app.get(url).json

    def test_post_user(self):
        data = {'name': 'Fulano Beltrano'}
        forecast_dict = {'address': 'Rua Marshmallow',
                         'notification': '07:00:00'}
        forecast_dict["period"] = {'period_from': '08:00:00',
                                   'period_to': '19:00:00'}
        forecast_dict["days"] = {'sunday': True,
                                 'monday': True,
                                 'tuesday': True,
                                 'wednesday': True,
                                 'thursday': True,
                                 'friday': False,
                                 'saturday': False}
        data["forecast"] = [forecast_dict]
        rv = self.app.post('/users', data=json.dumps(data),
                           content_type='application/json').json
        assert data == rv

    def test_update_user(self):
        user = User.create(name='Fulano teste')
        data = {'name': 'Teste update'}
        forecast_dict = {'address': 'Rua Marshmallow',
                         'notification': '07:00:00'}
        forecast_dict["period"] = {'period_from': '08:00:00',
                                   'period_to': '19:00:00'}
        forecast_dict["days"] = {'sunday': True,
                                 'monday': True,
                                 'tuesday': True,
                                 'wednesday': True,
                                 'thursday': True,
                                 'friday': False,
                                 'saturday': False}
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

    def test_forecast_get(self):
        user = User.create(name='Teste update')
        forecast_dict = {'user_id': user.id,
                         'address': 'Rua Marshmallow',
                         'notification': '07:00:00'}
        forecast_dict["period"] = {'period_from': '08:00:00',
                                   'period_to': '19:00:00'}
        forecast_dict["days"] = {'sunday': True,
                                 'monday': True,
                                 'tuesday': True,
                                 'wednesday': True,
                                 'thursday': True,
                                 'friday': False,
                                 'saturday': False}
        forecast = Forecast.create(user=user, **forecast_dict)
        Period.create(period=forecast, **forecast_dict["period"])
        Days.create(days=forecast, **forecast_dict["days"])
        forecast_dict["id"] = forecast.id
        url = "users/%s/forecast/%s" % (user.id, forecast.id)
        rv = self.app.get(url,
                          content_type='application/json').json
        assert forecast_dict == rv

        url = "users/1/forecast/540"
        rv = self.app.get(url,
                          content_type='application/json').json
        assert {"message": "Forecast could not be found"} == rv
