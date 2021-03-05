""" Flask Configuration """
from os import environ
import logging


class Config:
    """
    Base Config File
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_URI = environ.get("DATABASE_URL")
    DATABASE_PORT = environ.get("DATABASE_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """
    Development Configuration
    """
    TESTING = True
    DEBUG = True
    ENV = 'development'
    DATABASE_USER = 'postgres'
    DATABASE_NAME = 'mydb2'
    DATABASE_PASSWORD = '3366'
    DATABASE_URI = '127.0.0.1'
    DATABASE_PORT = 5432
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = "app.log"
    LOG_TYPE = logging.DEBUG


class ProdConfig(Config):
    """
    Production Environment Config FIle Configuration
    Environment Required Variable:
        variable         :     operation                 :      example
    ==================================================================================================================
        DATABASE_USER    : export user name              :       "root"
        DATABASE_NAME    : export name                   :       "mydb"
        DATABASE_PASSWORD: export DATABASE_USER password :       "xyz"
        DATABASE_URI     : export databse URI            :       dialect+driver://username:password@host:port/database
        DATABASE_PORT    : export port                   :       "5432"
    ==================================================================================================================
    """
    TESTING = False
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_USER = environ.get("DATABASE_USER")
    DATABASE_NAME = environ.get("DATABASE_NAME")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_URI = environ.get("DATABASE_URI")
    DATABASE_PORT = environ.get("DATABASE_PORT")
    LOG_FILE = "app.log"
    LOG_TYPE = logging.DEBUG
