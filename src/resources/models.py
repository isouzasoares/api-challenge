from peewee import (CharField, ForeignKeyField, TimeField,
                    PrimaryKeyField, BooleanField)
from app import db


class User(db.Model):
    id = PrimaryKeyField(null=False)
    name = CharField()


class Forecast(db.Model):
    id = PrimaryKeyField(null=False)
    user = ForeignKeyField(User, backref='user')
    address = CharField()
    notification = TimeField()


class Period(db.Model):
    period = ForeignKeyField(Forecast, backref='period',
                             primary_key=True)
    period_from = TimeField()
    period_to = TimeField()


class Days(db.Model):
    days = ForeignKeyField(Forecast, backref='days',
                           primary_key=True)
    sunday = BooleanField(default=False)
    monday = BooleanField(default=False)
    tuesday = BooleanField(default=False)
    wednesday = BooleanField(default=False)
    thursday = BooleanField(default=False)
    friday = BooleanField(default=False)
    saturday = BooleanField(default=False)
