from typing import Dict
from ..flask_setup.flask import app
from .dimension_reduction import DimensionReductionModel
from ..data.dataset import DatasetAlgorithmEnum
from ..data.exceptions import WrongAlgorithmException, WrongDatasetException
from ..data.data_loader import data_loader
import os


class DimensionReductionModelLoader(object):
    def __init__(self, datasets_path: str):
        self._models: Dict[str, Dict[str, DimensionReductionModel]] = {}
        for parent_file in os.scandir(datasets_path):
            if parent_file.is_dir():
                dataset_name = parent_file.name
                for file in os.scandir(f"{datasets_path}/{dataset_name}"):
                    file_name_list = file.name.split(".")
                    # we store both data and model files inside this dir
                    if file.is_file() and file_name_list[1] == "model":
                        self._models[dataset_name][
                            file_name_list[0]
                        ] = DimensionReductionModel(file.path)

    def get_models(self):
        return self._models

    def get_model(self, dataset_name: str, dataset_algorithm: DatasetAlgorithmEnum):
        self._check_valid_params(dataset_name, dataset_algorithm)
        return self._models[dataset_name][dataset_algorithm.value]

    def _check_valid_params(
        self, dataset_name: str, dataset_algorithm: DatasetAlgorithmEnum
    ):
        available_datasets = data_loader.get_datasets()
        if dataset_name not in available_datasets:
            raise WrongDatasetException(
                f"No such dataset, must be one of {available_datasets.keys()}"
            )
        if dataset_algorithm not in DatasetAlgorithmEnum.list_all():
            raise WrongAlgorithmException(
                f"No available samples for given algorithm, must be one of {DatasetAlgorithmEnum.list_all()}"
            )


reduction_models_loader = DimensionReductionModelLoader(app.config["DATASETS_PATH"])
