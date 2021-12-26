from enum import Enum
from typing import Dict, Union
import pickle


class DatasetAlgorithmEnum(Enum):
    PCA = "pca"
    UMAP = "umap"

    @classmethod
    def list_all(cls):
        return list(map(lambda c: c.value, cls))


class Dataset(object):
    def __init__(self, dataset_path: str, eager_load: bool = False):
        self.dataset_path = dataset_path
        self._datapoints: list[Dict] = [{}]
        self.loaded = False
        self.samples_count: Union[int, None] = None
        if eager_load:
            self.load()

    def load(self):
        with open(self.dataset_path, "rb") as datapoints_file:
            self._datapoints: list[Dict] = pickle.load(datapoints_file)
            self.loaded = True
            self.samples_count = len(self._datapoints)
        return self

    def get(self):
        return self._datapoints
