from __future__ import annotations
import pickle
from .data_object import DataObject
from typing import Dict


class Dataset(DataObject):
    def __init__(self, dataset_path: str, eager_load: bool = False):
        super().__init__(dataset_path, eager_load)
        self.samples_count = None

    def load(self):
        super().load()
        with open(self._object_path, "rb") as datapoints_file:
            self._datapoints: list[Dict] = pickle.load(datapoints_file)
            self.loaded = True
            self.samples_count = len(self._datapoints)

    def get(self):
        return self._datapoints
