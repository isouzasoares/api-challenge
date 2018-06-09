from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

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


class ForecastAdd(Resource):

    def post(self):
        json_input = request.get_json()
        try:
            data = forecast_schema.load(json_input)
            forecast = Forecast.create(user=data["user_id"],
                                       address=data["address"],
                                       notification=data["notification"])
            period = Period.create(period=forecast, **data["period"])
            days = Days.create(days=forecast, **data["days"])
            forecast_data = forecast_schema.dump(forecast)
            forecast_data["period"] = period_schema.dump(period)
            forecast_data["days"] = days_schema.dump(days)
            data = jsonify(forecast_data)
            data.status_code = 201
        except ValidationError as err:
            data = {'errors': err.messages}
            data.status_code = 422

        return data
