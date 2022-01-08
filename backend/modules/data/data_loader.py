import abc
import os
from .dataset import Dataset
from .dimension_reduction import DimensionReductionModel
from typing import Dict, Union


class DataLoader(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self, objects_path: str, is_dataset_load: bool, eager_load: bool = False
    ):
        self._objects: Dict[
            str, Dict[str, Union[Dataset, DimensionReductionModel]]
        ] = {}
        for parent_file in os.scandir(objects_path):
            if parent_file.is_dir():
                object_name = parent_file.name
                self._objects[object_name] = {}
                for file in os.scandir(f"{objects_path}/{object_name}"):
                    file_name_list = file.name.split(".")
                    # we store both data and model files inside this dir
                    if file.is_file():
                        if is_dataset_load and file_name_list[1] == "data":
                            self._objects[object_name][file_name_list[0]] = Dataset(
                                file.path, eager_load
                            )
                        elif not is_dataset_load and file_name_list[1] == "model":
                            self._objects[object_name][
                                file_name_list[0]
                            ] = DimensionReductionModel(file.path, eager_load)

    def get_objects(self):
        return self._objects

    def get_object(self, dataset_name: str, dataset_algorithm: str):
        data_entry = self._objects[dataset_name][dataset_algorithm]
        if not data_entry.loaded:
            data_entry.load()
        return data_entry

    def load_object(self, dataset_name: str, dataset_algorithm):
        data_entry = self._objects[dataset_name][dataset_algorithm]
        if not data_entry.loaded:
            data_entry.load()
