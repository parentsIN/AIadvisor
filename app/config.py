import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    TESTING = True

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig
)