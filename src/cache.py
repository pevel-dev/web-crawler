import pickle
import sys


class Cache:
    def __init__(self, save_path: str, cache):
        self._save_path = save_path
        self.cache = cache

    def save(self):
        try:
            pickle.dump(self.cache, self._save_path)
        except pickle.PicklingError as exception:
            print(f"Serialization error. It was not possible to save the cache to disk.\nError: {exception}")
            sys.exit(0)

    def load(self):
        try:
            self.cache = pickle.load(self._save_path)
        except pickle.UnpicklingError as exception:
            print(f"Serialization error. Failed to deserialize file.\nError: {exception}")
            sys.exit(0)
