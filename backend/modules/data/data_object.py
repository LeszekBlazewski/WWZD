import abc


class DataObject(abc.ABC):
    @abc.abstractmethod
    def __init__(self, object_path: str, eager_load: bool = False):
        self._object_path = object_path
        self.loaded = False
        if eager_load:
            self.load()

    @abc.abstractmethod
    def load(self):
        if self.loaded:
            print("already loaded")
            return
