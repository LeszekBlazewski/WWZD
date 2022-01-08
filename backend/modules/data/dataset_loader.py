from .data_loader import DataLoader
from ..flask_setup.flask import app


class DatasetLoader(DataLoader):
    def __init__(self, datasets_path: str, eager_dataset_load: bool = False):
        super().__init__(datasets_path, True, eager_dataset_load)

    def get_dataset_names(self):
        return list(self._objects.keys())


dataset_loader = DatasetLoader(
    app.config["DATASETS_PATH"], app.config["PREALOAD_DATASETS"]
)
