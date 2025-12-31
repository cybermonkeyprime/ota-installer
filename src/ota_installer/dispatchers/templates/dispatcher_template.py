# src/ota_installer/dispatchers/templates/dispatcher_template.py
from collections.abc import Callable
from dataclasses import field
from pathlib import Path
from typing import TypeVar

from ...log_setup import logger
from ..protocols.dispatcher_protocol import DispatcherProtocol

T = TypeVar("T")

CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]


class DispatcherTemplate(DispatcherProtocol):
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
        collection_value = self.collection[self.normalize_key(key)]
        return collection_value

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        try:
            task = self.collection[self.normalize_key(key)]
            if not isinstance(task, Callable):
                raise ValueError(
                    f"No task found for key: {self.normalize_key(key)}"
                )
            else:
                return task()
        except ValueError as err:
            logger.exception(f"{type(err).__name__} occurred at: {err}")
            return None

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()
