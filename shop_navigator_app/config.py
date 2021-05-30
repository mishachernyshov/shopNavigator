"""
The configuration modes for application running.
"""

import os


class BaseConfig:
    """
    The basic configuration settings for all other configurations.
    They add and/or override some specific settings that are appropriate
    for the situations they are intended.
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_CONNECTION_STRING')
    UPLOAD_FOLDER = 'images'


class DevelopmentConfig(BaseConfig):
    """
    The configuration for application running during development.
    """
    DEBUG = True
    TESTING = True


class TestConfig(BaseConfig):
    """
    The configuration for application running during testing.
    """
    TESTING = True
