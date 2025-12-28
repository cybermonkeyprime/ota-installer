# src/ota_installer/types/dispatcher_protocol.py
from typing import Protocol


class DispatcherProtocol(Protocol):
    def get_value(self, key: str) -> object: ...
