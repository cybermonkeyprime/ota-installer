# src/ota_installer/dispatcher/dispatcher_template.py
from collections.abc import Callable
from typing import cast

from ..log_setup import logger
from .dispatcher_protocol import DispatcherProtocol


class DispatcherTemplate(DispatcherProtocol):
    """
    A template class for dispatching tasks based on a key-value collection.
    """

    collection: dict = {}

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """

        normalized_key = self.normalize_key(key)
        result = self.collection.get(self.normalize_key(key))

        if result is None:
            message = f"Key not found in collection: {normalized_key}"
            logger.error(message)
            raise KeyError(message)

        return result

    def get_instance(self, key: str) -> Callable:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        normalized_key = self.normalize_key(key)
        callback = self.collection.get(normalized_key)

        if callback is None:
            message = f"Key not found in collection: {normalized_key}"
            logger.critical(message)
            raise KeyError(message)

        if not callable(callback):
            message = (
                "Expected a callable object, "
                f"but got {type(callback).__name__}"
            )
            logger.error(message)
            raise TypeError(message)
        return cast(Callable, callback)()

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()


# Signed off by Brian Sanford on 20260827
