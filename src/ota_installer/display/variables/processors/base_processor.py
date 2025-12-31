# src/ota_installer/display/variables/processors/base_processor.py
from dataclasses import dataclass, field

from ....types import DispatcherProtocol


@dataclass
class BaseProcessor(object):
    processing_function: object = field(init=False)
    dispatcher: DispatcherProtocol | None = field(init=False)
    dispatcher_type: str | None = None  # To be set in subclasses

    def __post_init__(self) -> None:
        if not self.dispatcher_type:
            raise ValueError(
                "dispatcher_type must be set in subclass before __post_init__"
            )
        self.dispatcher = self.processing_function.get_dispatcher(
            self.dispatcher_type
        )
        if not self.dispatcher:
            raise RuntimeError(
                f"Dispatcher creation failed for process type: {self.dispatcher_type}"
            )

    def get_value_by_key(self, key: str) -> object:
        return self.dispatcher.get_value(key)
