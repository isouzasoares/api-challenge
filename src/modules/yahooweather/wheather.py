import requests


FORECAST_MONITOR = ("1",
                    "4",
                    "5",
                    "6",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "17",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "35",
                    "37",
                    "38",
                    "39",
                    "40",
                    "42",
                    "41",
                    "44",
                    "45")


class YahooForecast:
    def __init__(self, types=None):
        self.url = "https://query.yahooapis.com/v1/public/yql?format=json&q="
        if not types:
            types = FORECAST_MONITOR
        self.types = types

    def get_query(self, location):
        query = """select item.forecast from weather.forecast where woeid in
                   (select woeid from geo.places(1)
                   where text="%s") and item.forecast.code in %s %s"""
        query = query % (location, self.types, "")
        return query

    def get_forecast_by_location(self, location):
        items = []
        url = "%s%s" % (self.url, self.get_query(location))
        items = requests.get(url)
        if items.status_code == 200:
            return items.json()["query"]["results"]["channel"]["item"][
                "forecast"]
        return items

    def get_forecast_location_period(self, location, period_from, period_to):
        forecast = self.get_forecast_by_location(location)
        for item in forecast:
            pass
