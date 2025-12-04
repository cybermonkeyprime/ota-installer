# src/dispatchers/templates/dispatcher_creator.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self, TypeVar

T = TypeVar("T")

CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]


@dataclass
class DispatcherCreator(object):
    """
    A centralized dispatcher class for dispatching tasks based on a key-value
    collection.
    """

    collection: CollectionDictionary = field(
        default_factory=CollectionDictionary
    )

    def set_collection(self, dictionary: dict) -> Self:
        self.collection = dictionary
        return self

    # @decorators.ExceptionHandler()
    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """
        task = self.collection[key]
        if isinstance(task, Callable):
            return task()
        else:
            raise ValueError(f"No task found for key: {key}")
