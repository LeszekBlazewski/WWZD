from __future__ import annotations
import pickle
from .data_object import DataObject


class DimensionReductionModel(DataObject):
    def __init__(self, model_path: str, eager_model_load: bool = False):
        super().__init__(model_path, eager_model_load)

    def transform(self, outputs_from_model):
        if not self.loaded:
            self.load()
        reduced_outputs: list[float] = self._model.transform(outputs_from_model)
        return reduced_outputs

    def load(self):
        super().load()
        with open(self._object_path, "rb") as model_file:
            self._model = pickle.load(model_file)
            self.loaded = True
