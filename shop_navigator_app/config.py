import os


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONNECTION_STRING')
    UPLOAD_FOLDER = 'images'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
