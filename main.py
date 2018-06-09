from app import app, db

from src.resources.models import User, Forecast, Period, Days


def create_tables():
    # Create table for each model if it does not exist.
    # Use the underlying peewee database object instead of the
    # flask-peewee database wrapper:
    db.database.create_tables([User, Forecast, Period, Days], safe=True)

if __name__ == '__main__':
    create_tables()
    app.run()
