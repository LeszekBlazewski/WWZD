from ...data.data_loader import data_loader, DatasetAlgorithmEnum
from ...model.dimension_reduction_loader import reduction_models_loader
from ...data.exceptions import WrongAlgorithmException, WrongDatasetException
from flask_restx import Resource, reqparse
from ..models.data_models import data_point_model, dataset_model, dataset_api


@dataset_api.errorhandler(WrongAlgorithmException)
@dataset_api.errorhandler(WrongDatasetException)
def handle_wrong_param_exception(error):
    return {"message": error.message}, 400


# TODO: Fix this check how the loop works
@dataset_api.route("/")
class DatasetResource(Resource):
    @dataset_api.doc("List available datasets")
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
    "algorithm",
    choices=DatasetAlgorithmEnum.list_all(),
    required=True,
    type=str,
    help="Name of algorithm that has been used for dataset",
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

parser_dataset_load = reqparse.RequestParser()

parser_dataset_load.add_argument(
    "algorithm",
    choices=[DatasetAlgorithmEnum.list_all(), None],
    type=str,
    help="Name of algorithm that has been used for dataset. If None datapoints for all available models will be loaded",
)


@dataset_api.route(
    "/<string:dataset_name>",
    doc={
        "params": {
            "dataset_name": f"One of the following: {data_loader.get_datasets().keys()}"
        }
    },
)
class DataPointResource(Resource):
    @dataset_api.doc("List classified data points")
    @dataset_api.expect(parser)
    @dataset_api.marshal_list_with(data_point_model)
    def get(self, dataset_name):
        request_args = parser.parse_args()
        algorithm = request_args["algorithm"].upper()
        start = request_args["start"]
        stop = request_args["stop"]
        dataset_data = data_loader.get_classification_dataset(
            dataset_name, DatasetAlgorithmEnum[algorithm]
        )
        return dataset_data[start:stop]

    @dataset_api.doc("Load given dataset or datasets")
    @dataset_api.expect(parser_dataset_load)
    @dataset_api.marshal_with(dataset_model)
    def post(self, dataset_name):
        loaded_entry = data_loader.load_classification_dataset(dataset_name)
        return {"name": dataset_name, "samples": loaded_entry.samples_count}
