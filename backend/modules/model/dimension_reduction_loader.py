from typing import Dict
from ..flask_setup.flask import app
from .dimension_reduction import DimensionReductionModel
from ..data.exceptions import WrongAlgorithmException, WrongDatasetException
import os


class DimensionReductionModelLoader(object):
    def __init__(self, datasets_path: str):
        self._models: Dict[str, Dict[str, DimensionReductionModel]] = {}
        for parent_file in os.scandir(datasets_path):
            if parent_file.is_dir():
                dataset_name = parent_file.name
                self._models[dataset_name] = {}
                for file in os.scandir(f"{datasets_path}/{dataset_name}"):
                    file_name_list = file.name.split(".")
                    # we store both data and model files inside this dir
                    if file.is_file() and file_name_list[1] == "model":
                        self._models[dataset_name][
                            file_name_list[0]
                        ] = DimensionReductionModel(file.path)

    def get_models(self):
        return self._models

    def get_reduction_models_for_dataset(self, dataset_name: str):
        models_for_dataset = self._models[dataset_name]
        return list(models_for_dataset.keys())

    def get_model(self, dataset_name: str, dataset_algorithm: str):
        self._check_valid_params(dataset_name, dataset_algorithm)
        return self._models[dataset_name][dataset_algorithm]

    def _check_valid_params(self, dataset_name: str, dataset_algorithm: str):
        if dataset_name not in self._models:
            raise WrongDatasetException(
                f"No such dataset, must be one of {list(self._models.keys())}"
            )
        if dataset_algorithm not in self.get_reduction_models_for_dataset(dataset_name):
            raise WrongAlgorithmException(
                f"No available samples for given algorithm, must be one of {self.get_reduction_models_for_dataset(dataset_name)}"
            )


reduction_models_loader = DimensionReductionModelLoader(app.config["DATASETS_PATH"])
