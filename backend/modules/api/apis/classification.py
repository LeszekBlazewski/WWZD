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


@classification_api.route("/")
class ClassificationResource(Resource):
    @classification_api.doc("Classify given sample")
    @classification_api.expect(parser)
    @classification_api.marshal_with(data_point, code=201)
    def post(self):
        request_args = parser.parse_args()
        algorithm = request_args["algorithm"].upper()
        # TODO: Use our bert model + pca/umap to classify and return the sample
        return (
            {
                "text": "Explanation\nWhy the edits made under my username Hardcore Metallica Fan were reverted? They weren't vandalisms, just closure on some GAs after I voted at New York Dolls FAC. And please don't remove the template from the talk page since I'm retired now.89.205.38.27",
                "position": {"x": -3.3748245, "y": -0.37758058},
                "classification": {
                    "toxic": False,
                    "severeToxic": False,
                    "obscene": False,
                    "threat": False,
                    "insult": False,
                    "identityHate": False,
                },
            },
        ), 201
