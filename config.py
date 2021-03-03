""" Flask Configuration """
from os import environ


class Config:
    """
    Base Config File
    """
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'


class DevConfig(Config):
    """
    Development Environment Configuration
    """
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'development'


class ProdConfig(Config):
    """
    Production Environment Configuration
    """
    TESTING = False
    DEBUG = False
    FLASK_ENV = 'production'
    DATABASE_URL = environ.get("PROD_DATABASE_URI")

