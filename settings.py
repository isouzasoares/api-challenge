class BaseConfig(object):
    DEBUG = False
    TESTING = False
    DEBUG = False
    SECRET_KEY = 'ssshhhh'
    DATABASE = {
        'name': 'example.db',
        'engine': 'peewee.SqliteDatabase'}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    DATABASE = {
        'name': 'test.db',
        'engine': 'peewee.SqliteDatabase'}
