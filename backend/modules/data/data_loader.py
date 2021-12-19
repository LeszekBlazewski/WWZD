from enum import Enum
from typing import Dict
from flask_restx import marshal
from ..api.models.datapoint import data_point
from ..flask_setup.flask import app
import os
import json


class DatasetAlgorithm(Enum):
    PCA = "pca"
    UMAP = "umap"

    @classmethod
    def list_all(cls):
        return list(map(lambda c: c.value, cls))


class DataLoader(object):
    def __init__(self, datasets_path: str):
        self.datasets_path = datasets_path
        self.datasets: Dict[str, Dict[str, object]] = {}
        self.available_datasets = [
            f.name for f in os.scandir(datasets_path) if f.is_dir()
        ]

    def get_available_classification_datasets(self):
        return self.available_datasets

    def get_classification_dataset(
        self, dataset_name: str, dataset_algorithm: DatasetAlgorithm
    ):
        if dataset_name in self.datasets:
            data_entry = self.datasets[dataset_name]
            if dataset_algorithm == DatasetAlgorithm.PCA:
                return data_entry[DatasetAlgorithm.PCA.value]
            elif dataset_algorithm == DatasetAlgorithm.UMAP:
                return data_entry[DatasetAlgorithm.UMAP.value]
            else:
                raise ValueError("No such dataset algorithm")

        loaded_entry = self._load_classification_datasets(dataset_name)
        return (
            loaded_entry[DatasetAlgorithm.PCA.value]
            if dataset_algorithm == DatasetAlgorithm.PCA
            else loaded_entry[DatasetAlgorithm.UMAP.value]
        )

    def _load_classification_datasets(self, dataset_name: str):
        dataset_path = f"{self.datasets_path}/{dataset_name}"
        with open(
            f"{dataset_path}/{DatasetAlgorithm.PCA.value}.json"
        ) as pca_file, open(
            f"{dataset_path}/{DatasetAlgorithm.UMAP.value}.json"
        ) as umap_file:
            pca_json = json.load(pca_file)
            umap_json = json.load(umap_file)
            pca_results = marshal(pca_json, data_point)
            umap_results = marshal(umap_json, data_point)
            data_entry = {
                DatasetAlgorithm.PCA.value: pca_results,
                DatasetAlgorithm.UMAP.value: umap_results,
            }
            self.datasets[dataset_name] = data_entry
        return data_entry


data_loader = DataLoader(app.config["DATASETS_PATH"])
