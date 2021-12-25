from flask_restx import Namespace, Resource, reqparse
from .dataset_api import data_point_model
from ...data.data_loader import DatasetAlgorithm
from ...model.model import model
from ...model.dimension_reduction_loader import reduction_models_loader
from ...flask_setup.flask import app


classification_api = Namespace(
    "classification", description="Operations regarding classification of new samples"
)

parser = reqparse.RequestParser()
parser.add_argument(
    "algorithm",
    choices=DatasetAlgorithm.list_all(),
    required=True,
    type=str,
    help="Name of algorithm that should be used to locate given sample",
)
parser.add_argument(
    "text",
    required=True,
    type=str,
    help="Text which should be classified",
)

# TODO: Fix this to accept list of text (input field as json not param)
@classification_api.route("/")
class ClassificationResource(Resource):
    @classification_api.doc("Classify given samples")
    @classification_api.expect(parser)
    @classification_api.marshal_with(data_point_model, code=201)
    def post(self):
        request_args = parser.parse_args()
        algorithm = request_args["algorithm"].upper()
        text = request_args["text"]
        (last_layer_outputs, predictions) = model.predict([text])
        reduction_model = reduction_models_loader.get_model(algorithm)
        positions = reduction_model.transform(last_layer_outputs)
        response_classification_fields = [
            "toxic",
            "severeToxic",
            "obscene",
            "threat",
            "insult",
            "identityHate",
        ]
        label_list = app.config["LABEL_LIST"]
        response = {
            "text": text,
            "position": {"x": positions[0], "y": positions[1]},
        }
        for index, class_label in enumerate(label_list):
            response["classification"][response_classification_fields[index]] = {
                "assigned": bool(round(predictions[0][class_label])),
                "prediction": round(predictions[0][class_label] * 100, 2),
            }
        return response, 200
