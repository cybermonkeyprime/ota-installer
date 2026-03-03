# src/ota_installer/types/dispatcher_protocol.py
from typing import Protocol


class DispatcherProtocol(Protocol):
    """A protocol for dispatching key-value retrieval."""

    def get_value(self, key: str) -> object: ...


