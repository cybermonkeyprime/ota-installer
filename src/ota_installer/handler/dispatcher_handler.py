# src/ota_installer/handler/dispatcher_handler.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol, runtime_checkable

from ..log_setup import logger

CollectionKeys = str
CollectionValues = Path | str
CollectionDictionary = dict[CollectionKeys, CollectionValues]


@runtime_checkable
class DispatcherProtocol(Protocol):
    """
    Protocol defining the interface expected of all dispatchers.
    Ensures compatibility across dispatcher variants and promotes consistent
    behavior.
    """

    collection: dict[str, object]

    def get_value(self, key: str) -> object:
        """
        Retrieve a value from the internal collection using the provided key.
        """
        ...

    def get_instance(self, key: str) -> object | None:
        """Retrieve an instance from the collection using the provided key."""
        ...

    @staticmethod
    def normalize_key(key: str) -> str:
        """
        Normalize a key string for consistent internal usage.
        Typical implementations may use lowercasing, stripping, or other
        formatting.
        """
        ...


class DispatcherTemplate(DispatcherProtocol):
    """
    A template class for dispatching tasks based on a key-value collection.
    """

    collection: CollectionDictionary = field(default_factory=dict)

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """
        if result := self.collection.get(self.normalize_key(key)):
            logger.exception(f"Value is {key} not found")
            raise

        return result

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        normalized_key = self.normalize_key(key)
        task = self.collection.get(normalized_key)

        if task is None:
            logger.critical(f"Key not found in collection: {normalized_key}")
            return None

        if not callable(task):
            logger.error(
                f"Value for '{normalized_key}' is not a callable task."
            )
            return None
        return task()

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()


# Signed off by Brian Sanford on 20260523
