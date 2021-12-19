import os


class Config(object):
    HOST = "0.0.0.0"
    PORT = "8081"
    ENV = os.getenv("ENV")
    MODELS_PATH = os.getenv("MODELS_PATH")  # From Dockerfile
    # DATASETS_PATH = os.getenv("DATASETS_PATH")  # From Dockerfile
    DATASETS_PATH = "./datasets"
    USE_CPU = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
