from flask_restx import Api
from flask import Blueprint
from .apis.classification_api import classification_api
from .apis.dataset_api import dataset_api
from ..flask_setup.flask import app


blueprint = Blueprint("api", __name__, url_prefix=app.config["API_URL"])

api = Api(
    blueprint,
    title="Toxic API",
    version="1.0",
    description="Toxic phrases classification API",
    doc="/" if app.config["ENABLE_SWAGGER"] == True else False,
)

api.add_namespace(dataset_api)
api.add_namespace(classification_api)
