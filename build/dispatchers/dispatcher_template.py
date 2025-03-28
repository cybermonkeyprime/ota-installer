from collections.abc import Callable
from typing import Optional, Union
from pathlib import Path
from dataclasses import field

CollectionDictionary = Union[type, Path, None]


class DispatcherTemplate:
    collection: dict[str, CollectionDictionary] = field(default_factory=lambda: {})

    def get_value(self, key: str) -> CollectionDictionary:
        return self.collection.get(key)

    def get_instance(self, key: str) -> Optional[Callable]:
        try:
            task = self.get_value(key)
            if task is not None:
                return task()
            else:
                raise ValueError(f"No task found for key: {key}")
        except ValueError as err:
            print(err)
            return None
