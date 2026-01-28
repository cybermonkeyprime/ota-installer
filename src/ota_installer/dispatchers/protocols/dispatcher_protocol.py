# src/ota_installer/dispatchers/protocols/dispatcher_protocol.py
from typing import Protocol, runtime_checkable


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

    def get_instance(self, key: str) -> object | None: ...

    @staticmethod
    def normalize_key(key: str) -> str:
        """
        Normalize a key string for consistent internal usage.
        Typical implementations may use lowercasing, stripping, or other
        formatting.
        """
        ...


