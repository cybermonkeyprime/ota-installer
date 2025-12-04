from collections.abc import Callable
from dataclasses import field
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")

CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]


class DispatcherTemplate(object):
    """
    A template class for dispatching tasks based on a key-value collection.
    """

    collection: CollectionDictionary = field(
        default_factory=CollectionDictionary
    )

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """
        collection_value = self.collection[key]
        return collection_value

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        try:
            task = self.get_value(key)
            if isinstance(task, Callable):
                return task()
            else:
                raise ValueError(f"No task found for key: {key}")
        except ValueError as err:
            print(f"Error occurred at: {err}")
            return None
