from typing import Dict
from ..flask_setup.flask import app
from .dimension_reduction import DimensionReductionModel
from ..data.dataset import DatasetAlgorithm
from ..data.exceptions import WrongAlgorithmException
import os


class DimensionReductionModelLoader(object):
    def __init__(self, models_path: str):
        self._models: Dict[str, DimensionReductionModel] = {}
        for file in os.scandir(models_path):
            if file.is_file():
                model_name = file.name.split(".")[1]
                self._models[model_name] = DimensionReductionModel(file.path)

    def get_model(self, dataset_algorithm: DatasetAlgorithm):
        self._check_if_valid_algorithm(dataset_algorithm)
        return self._models[dataset_algorithm.value]

    def _check_if_valid_algorithm(self, dataset_algorithm: DatasetAlgorithm):
        if dataset_algorithm not in DatasetAlgorithm.list_all():
            raise WrongAlgorithmException(
                f"No available samples for given algorithm, must be one of {DatasetAlgorithm.list_all()}"
            )


reduction_models_loader = DimensionReductionModelLoader(
    app.config["DIMENSION_REDUCTION_MODELS_PATH"]
)
