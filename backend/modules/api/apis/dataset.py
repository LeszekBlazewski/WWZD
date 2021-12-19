from ...data.data_loader import data_loader, DatasetAlgorithm
from flask_restx import Resource, fields, reqparse
from ..models.datapoint import data_point, dataset_api


parser = reqparse.RequestParser()

parser.add_argument(
    "algorithm",
    choices=DatasetAlgorithm.list_all(),
    required=True,
    type=str,
    help="Name of algorithm that has been used for dataset",
)
parser.add_argument("limit", type=int, help="How many samples should be fetched")


@dataset_api.route("/")
class DatasetResource(Resource):
    @dataset_api.doc("List available datasets")
    @dataset_api.response(
        200,
        "List of available datasets that can be queried",
        fields.List(fields.String),
    )
    def get(self):
        return data_loader.get_available_classification_datasets()


@dataset_api.route(
    "/<string:dataset_name>",
    doc={
        "params": {
            "dataset_name": f"One of the following: {data_loader.get_available_classification_datasets()}"
        }
    },
)
class DataPointResource(Resource):
    @dataset_api.doc("List classified data points")
    @dataset_api.expect(parser)
    @dataset_api.marshal_list_with(data_point)
    def get(self, dataset_name):
        request_args = parser.parse_args()
        # dataset_name = request_args["dataset_name"]
        algorithm = request_args["algorithm"].upper()
        limit = request_args["limit"]
        dataset_data = data_loader.get_classification_dataset(
            dataset_name, DatasetAlgorithm[algorithm]
        )
        if limit:
            dataset_data = dataset_data[:limit]
        return dataset_data
