import unittest

from app import create_app, create_db, create_resources
from main import create_tables
from modules.yahooweather.wheather import YahooForecast


class ApiTest(unittest.TestCase):

    def setUp(self):
        app = create_app("settings.TestingConfig")
        self.db = create_db(app)
        create_resources(app)
        self.app = app.test_client()
        with app.app_context():
            create_tables()

    def test_yahoo_request(self):
        yahoo = YahooForecast()
        items = yahoo.get_forecast_by_location("belo horizonte, br")
        assert items != []
        items = yahoo.get_forecast_by_location("barreiro, bh, br")
        assert items != []
