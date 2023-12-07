import pickle
import sys


class Cache:
    def __init__(self, save_path: str, cache):
        self._save_path = save_path
        self.cache = cache

    def save(self):
        try:
            with open(self._save_path, 'wb+') as f:
                pickle.dump(self.cache, f, fix_imports=True)
        except pickle.PicklingError as exception:
            print(f"Serialization error. It was not possible to save the cache to disk.\nError: {exception}")
            sys.exit(0)

    def load(self):
        try:
            with open(self._save_path, 'rb') as f:
                self.cache = pickle.load(f, encoding="utf-8")
        except EOFError:
            pass
        except FileNotFoundError as _:
            pass
        except pickle.UnpicklingError as exception:
            print(f"Serialization error. Failed to deserialize file.\nError: {exception}")
            sys.exit(0)
