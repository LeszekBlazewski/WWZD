from ...data.data_loader import data_loader
from ...model.dimension_reduction_loader import reduction_models_loader
from ...data.exceptions import WrongAlgorithmException, WrongDatasetException
from flask_restx import Resource, abort, reqparse
from ..models.data_models import (
    data_point_model,
    dataset_model,
    dataset_api,
    dataset_load_input,
    dataset_load_response,
)


@dataset_api.errorhandler(WrongAlgorithmException)
@dataset_api.errorhandler(WrongDatasetException)
def handle_wrong_param_exception(error):
    return {"message": error.message}, 400


def validate_input(dataset_name: str, algorithm: str):
    if dataset_name not in data_loader.get_dataset_names():
        abort(
            400,
            f"Wrong datasetName, must be one of: {data_loader.get_dataset_names()}",
        )
    if (
        algorithm
        and algorithm
        not in reduction_models_loader.get_reduction_models_for_dataset(dataset_name)
    ):
        abort(
            400,
            f"Wrong algorithm name, must be one of: {reduction_models_loader.get_reduction_models_for_dataset(dataset_name)}",
        )


@dataset_api.route("/")
class DatasetResourceList(Resource):
    @dataset_api.doc(description="List available datasets")
    @dataset_api.response(200, "Available datasets to query", dataset_model)
    @dataset_api.marshal_list_with(dataset_model)
    def get(self):
        reduced_datasets = []
        datasets = data_loader.get_datasets()
        reduction_models = reduction_models_loader.get_models()
        for key in datasets.keys() & reduction_models.keys():
            # we simply take number of samples from first dataset of model (all have same number of samples)
            samples_count = list(datasets[key].values())[0].samples_count
            reduced_datasets.append(
                {
                    "name": key,
                    "samplesCount": samples_count,
                    "availableReductionModels": [
                        m for m in reduction_models[key].keys()
                    ],
                }
            )
        return reduced_datasets


parser = reqparse.RequestParser()

parser.add_argument(
    "availableReductionModel",
    required=True,
    type=str,
    help="Name of algorithm that has been used for dataset from /datasets endpoint",
)
parser.add_argument(
    "start",
    type=int,
    help="Where to start when slicing the dataset (index of beginning sample), supports python slicing, leave empty for first",
)
parser.add_argument(
    "stop",
    type=int,
    help="Where to stop when slicing the datasets (index of last sample), suports python slicing, leave empty for last",
)


@dataset_api.route(
    "/<string:dataset_name>",
    doc={
        "params": {
            "dataset_name": f"One of the following: {data_loader.get_dataset_names()}"
        }
    },
)
class DatasetResource(Resource):
    @dataset_api.doc(description="List classified data points")
    @dataset_api.expect(parser)
    @dataset_api.marshal_list_with(data_point_model)
    def get(self, dataset_name: str):
        request_args = parser.parse_args()
        algorithm = request_args["availableReductionModel"]
        start = request_args["start"]
        stop = request_args["stop"]
        validate_input(dataset_name, algorithm)
        dataset_data = data_loader.get_classification_dataset(
            dataset_name, algorithm
        ).get()
        return dataset_data[start:stop]


@dataset_api.route("/load")
class DatasetLoadResource(Resource):
    @dataset_api.doc(
        description=f"Load sample set or sets for given dataset\n\ndatasetName one from:{data_loader.get_dataset_names()}\n\navailableReductionModel: Name of the algorithm from /datasets endpoint which was used to reduce data dimension. If no algorithm specified, samples for all available algorithms will be loaded"
    )
    @dataset_api.response(
        200, "Dataset/s loaded and details returned", dataset_load_response
    )
    @dataset_api.expect(dataset_load_input)
    @dataset_api.marshal_with(dataset_load_response)
    def post(self):
        dataset_name = dataset_api.payload["datasetName"]
        if "availableReductionModel" in dataset_api.payload:
            algorithm = dataset_api.payload["availableReductionModel"]
        else:
            algorithm = None
        validate_input(dataset_name, algorithm)
        loaded_entry = data_loader.load_classification_dataset(dataset_name, algorithm)
        reduction_models = reduction_models_loader.get_reduction_models_for_dataset(
            dataset_name
        )
        return {
            "datasetDetails": {
                "name": dataset_name,
                "samplesCount": loaded_entry.samples_count,
                "availableReductionModels": reduction_models,
            },
            "status": "partial" if algorithm else "all",
        }
