import os


class Config(object):
    HOST = "0.0.0.0"
    PORT = "8081"
    ENV = os.getenv("ENV")
    LABEL_LIST = [
        "toxic",
        "severe_toxic",
        "obscene",
        "threat",
        "insult",
        "identity_hate",
    ]
    USE_CPU = True  # model will be evaluated on CPU not CUDA
    PREALOAD_DATASETS = True  # If all datasets should be loaded at start
    BATCH_SIZE = 64  # when loading data to classify, how big should the batches be
    MAX_SEQ_LENGTH = 256  # what is the maximal character length of one sample
    ASSETS_PATH = os.getenv("ASSETS_PATH")  # From Dockerfile
    DATASETS_PATH = os.getenv("DATASETS_PATH")  # From Dockerfile
    # Based on the tar archive strśucture from google drive
    BERT_MODEL_PATH = f"{ASSETS_PATH}/bert"
    SWAGGER_UI_DOC_EXPANSION = "list"


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    TESTING = True


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
