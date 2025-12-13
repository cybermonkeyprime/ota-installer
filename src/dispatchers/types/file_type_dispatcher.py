from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, TypeVar

from src.dispatchers.templates import DispatcherCreator

T = TypeVar("T")

CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]
CollectionEnum = Literal


@dataclass
class FileTypeDispatcher(object):
    obj: type = field(default_factory=lambda: type)

    collection: dict = field(init=False, default_factory=dict)
    """
    A File dispatcher class for dispatching tasks based on a key-value
    collection.
    """

    def __post_init__(self) -> None:
        for element in {"PAYLOAD", "STOCK", "MAGISK"}:
            self.collection[element] = self.obj.paths.get(element.lower())

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """
        return self.collection[key.upper()]

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """
        return (
            DispatcherCreator()
            .set_collection(self.collection)
            .get_instance(key)
        )
