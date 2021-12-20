from flask_restx import Namespace, Resource, reqparse
from .dataset import data_point
from ...data.data_loader import DatasetAlgorithm


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


@classification_api.route("/")
class ClassificationResource(Resource):
    @classification_api.doc("Classify given sample")
    @classification_api.expect(parser)
    @classification_api.marshal_with(data_point, code=201)
    def post(self):
        request_args = parser.parse_args()
        algorithm = request_args["algorithm"].upper()
        text = request_args["text"]
        # TODO: Use our bert model + pca/umap to classify and return the sample
        return (
            {
                "text": text,
                "position": {"x": -3.3748245, "y": -0.37758058},
                "classification": {
                    "toxic": True,
                    "severeToxic": False,
                    "obscene": False,
                    "threat": False,
                    "insult": False,
                    "identityHate": False,
                },
            },
        ), 201
