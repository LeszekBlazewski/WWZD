from typing import Dict, Union
from .dataset import Dataset
from .exceptions import WrongAlgorithmException, WrongDatasetException
from .dataset import DatasetAlgorithm
from ..flask_setup.flask import app
import os


class DataLoader(object):
    def __init__(self, datasets_path: str, eager_dataset_load: bool = False):
        self._datasets: Dict[str, Dict[str, Dataset]] = {}
        for parent_file in os.scandir(datasets_path):
            if parent_file.is_dir():
                dataset_name = parent_file.name
                for datset_file in os.scandir(f"{datasets_path}/{dataset_name}"):
                    if datset_file.is_file():
                        model_name = datset_file.name.split(".")[1]
                        self._datasets[dataset_name][model_name] = Dataset(
                            datset_file.path, eager_dataset_load
                        )

    def get_datasets(self):
        return self._datasets

    def get_classification_dataset(
        self, dataset_name: str, dataset_algorithm: DatasetAlgorithm
    ):
        self._check_if_valid_dataset(dataset_name, dataset_algorithm)
        data_entry = self._datasets[dataset_name][dataset_algorithm.value]

        if not data_entry.loaded:
            data_entry.load()

        return data_entry

    def load_classification_dataset(
        self, dataset_name: str, dataset_algorithm: DatasetAlgorithm = None
    ) -> Dict[str, Union[str, int]]:
        self._check_if_valid_dataset(dataset_name, dataset_algorithm)
        if dataset_algorithm:
            entry = self._datasets[dataset_name][dataset_algorithm.value].load()
            return {"name": dataset_name, "samples": entry.samples_count}
        else:
            # load all of the available datapoints from different models
            for dataset in self._datasets[dataset_name].values():
                entry = dataset.load()
            return {"name": dataset_name, "samples": entry.samples_count}

    def _check_if_valid_dataset(
        self, dataset_name: str, dataset_algorithm: DatasetAlgorithm = None
    ):
        if dataset_name not in self._datasets:
            raise WrongDatasetException(
                f"No such dataset, must be one of {self.get_datasets().keys()}"
            )
        if dataset_algorithm and dataset_algorithm not in DatasetAlgorithm.list_all():
            raise WrongAlgorithmException(
                f"No available samples for given algorithm, must be one of {DatasetAlgorithm.list_all()}"
            )


data_loader = DataLoader(app.config["DATASETS_PATH"], app.config["PREALOAD_DATASETS"])
