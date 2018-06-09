from marshmallow import Schema, fields
from marshmallow import ValidationError


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class UserSchema(Schema):
    name = fields.Str(required=True)

user_schema = UserSchema()


class PeriodSchema(Schema):
    period_from = fields.Time(required=True)
    period_to = fields.Time(required=True)

period_schema = PeriodSchema()


class DaysSchema(Schema):
    sunday = fields.Boolean()
    monday = fields.Boolean()
    tuesday = fields.Boolean()
    wednesday = fields.Boolean()
    thursday = fields.Boolean()
    friday = fields.Boolean()
    saturday = fields.Boolean()

days_schema = DaysSchema()


class ForecastSchema(Schema):
    user_id = fields.Int()
    id = fields.Int(required=False)
    address = fields.Str(required=True)
    notification = fields.Time(required=True)
    period = fields.Nested(PeriodSchema, validate=must_not_be_blank)
    days = fields.Nested(DaysSchema, validate=must_not_be_blank)

forecast_schema = ForecastSchema()
forecastuser_schema = ForecastSchema(many=True)
