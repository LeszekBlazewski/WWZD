import os


class Config(object):
    HOST = "0.0.0.0"
    PORT = "8081"
    ENV = os.getenv("ENV")
    MODEL_PATH = os.getenv("MODEL_PATH") # From Dockerfile


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
