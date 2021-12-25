from ..flask_setup.flask import app
import pickle


class DimensionReductionModel(object):
    def __init__(self, model_path: str):
        self._load(model_path)

    def transform(self, outputs_from_model):
        reduced_outputs: list[float] = self._model.transform(outputs_from_model)
        return reduced_outputs

    def _load(self, model_path: str):
        with open(model_path, "rb") as model_file:
            self._model = pickle.load(model_file)
