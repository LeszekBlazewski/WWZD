from .data_loader import DataLoader
from ..flask_setup.flask import app


class DimensionReductionModelLoader(DataLoader):
    def __init__(self, datasets_path: str, eager_model_load: bool = False):
        super().__init__(datasets_path, False, eager_model_load)

    def get_reduction_models_for_dataset(self, dataset_name: str):
        models_for_dataset = self._objects[dataset_name]
        return list(models_for_dataset.keys())


reduction_models_loader = DimensionReductionModelLoader(app.config["DATASETS_PATH"])
