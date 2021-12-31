from flask_restx import Api
from .apis.classification_api import classification_api
from .apis.dataset_api import dataset_api

api = Api(
    title="Toxic API",
    version="1.0",
    description="Toxic phrases classification API",
)

api.add_namespace(dataset_api)
api.add_namespace(classification_api)
