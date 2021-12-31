from typing import Dict
from .dataset import Dataset
from .exceptions import WrongAlgorithmException, WrongDatasetException
from ..flask_setup.flask import app
from ..model.dimension_reduction_loader import reduction_models_loader
import os


class DataLoader(object):
    def __init__(self, datasets_path: str, eager_dataset_load: bool = False):
        self._datasets: Dict[str, Dict[str, Dataset]] = {}
        for parent_file in os.scandir(datasets_path):
            if parent_file.is_dir():
                dataset_name = parent_file.name
                self._datasets[dataset_name] = {}
                for file in os.scandir(f"{datasets_path}/{dataset_name}"):
                    file_name_list = file.name.split(".")
                    # we store both data and model files inside this dir
                    if file.is_file() and file_name_list[1] == "data":
                        self._datasets[dataset_name][file_name_list[0]] = Dataset(
                            file.path, eager_dataset_load
                        )

    def get_datasets(self):
        return self._datasets

    def get_dataset_names(self):
        return list(self._datasets.keys())

    def get_classification_dataset(self, dataset_name: str, dataset_algorithm: str):
        self._check_if_valid_dataset(dataset_name, dataset_algorithm)
        data_entry = self._datasets[dataset_name][dataset_algorithm]

        if not data_entry.loaded:
            data_entry.load()

        return data_entry

    def load_classification_dataset(
        self, dataset_name: str, dataset_algorithm: str = None
    ) -> Dataset:
        self._check_if_valid_dataset(dataset_name, dataset_algorithm)
        if dataset_algorithm:
            entry = self._datasets[dataset_name][dataset_algorithm].load()
        else:
            # load all of the available datapoints from different models
            for dataset in self._datasets[dataset_name].values():
                entry = dataset.load()
        return entry

    def _check_if_valid_dataset(self, dataset_name: str, dataset_algorithm: str = None):
        if dataset_name not in self._datasets:
            raise WrongDatasetException(
                f"No such dataset, must be one of {self.get_dataset_names()}"
            )
        if (
            dataset_algorithm
            and dataset_algorithm
            not in reduction_models_loader.get_reduction_models_for_dataset(
                dataset_name
            )
        ):
            raise WrongAlgorithmException(
                f"No available samples for given algorithm, must be one of {reduction_models_loader.get_reduction_models_for_dataset(dataset_name)}"
            )


data_loader = DataLoader(app.config["DATASETS_PATH"], app.config["PREALOAD_DATASETS"])
