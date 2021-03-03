""" Flask Configuration """
from os import environ


class Config:
    """
    Base Config File
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_URL = environ.get("DATABASE_URI")
    DATABASE_PORT = environ.get("DATABASE_PORT")


class DevConfig(Config):
    """
    Development Environment Configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_URL = environ.get("DATABASE_URI")
    DATABASE_PORT = environ.get("DATABASE_PORT")


class ProdConfig(Config):
    """
    Production Environment Configuration
    """
    TESTING = False
    DEBUG = False
    ENV = 'production'
    DATABASE_URL = environ.get("DATABASE_URI")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_PORT = environ.get("DATABASE_PORT")

