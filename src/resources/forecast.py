from flask import jsonify
from flask_restful import Resource

from .schema import forecast_schema, days_schema, period_schema
from .models import Forecast, Period, Days


class ForecastView(Resource):

    def get(self, user_id, forecast_id):
        try:
            forecast = Forecast.get(user=user_id, id=forecast_id)
            period = Period.get(period=forecast_id)
            days = Days.get(days=forecast_id)
            forecast_data = forecast_schema.dump(forecast)
            forecast_data["period"] = period_schema.dump(period)
            forecast_data["days"] = days_schema.dump(days)
            data = jsonify(forecast_data)
            data.status_code = 200
        except Forecast.DoesNotExist:
            data = jsonify({"message": "Forecast could not be found"})
            data.status_code = 404

        return data
