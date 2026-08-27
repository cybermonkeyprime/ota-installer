# src/ota_installer/dispatcher/dispatcher_protocol.py
from typing import Protocol, runtime_checkable


@runtime_checkable
class DispatcherProtocol(Protocol):
    """Protocol defining the interface expected of all dispatchers."""

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
        """Normalize a key string for consistent internal usage."""
        ...


# Signed off by Brian Sanford on 20260827
