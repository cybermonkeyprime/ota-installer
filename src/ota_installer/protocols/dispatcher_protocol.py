# src/ota_installer/types/dispatcher_protocol.py
from collections.abc import Callable

type DispatcherProtocol = Callable[[str], object]
