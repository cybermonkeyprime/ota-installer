# src/ota_installer/display/variables/processors/base_processor.py
from dataclasses import dataclass, field

from ....types.dispatcher_protocol import DispatcherProtocol


@dataclass
class BaseProcessor(object):
    """Base class for processing with a dispatcher."""

    processing_function: object = field(init=False)
    dispatcher: DispatcherProtocol | None = field(init=False)
    dispatcher_type: str | None = None  # To be set in subclasses

    def __post_init__(self) -> None:
        """Initializes the dispatcher based on the dispatcher type."""
        if not self.dispatcher_type:
            raise ValueError(
                "dispatcher_type must be set in subclass before __post_init__"
            )

        self.dispatcher = self.processing_function.get_dispatcher(
            self.dispatcher_type
        )

        if not self.dispatcher:
            raise RuntimeError(
                "Dispatcher creation failed for process type: "
                "f{self.dispatcher_type}"
            )

    def get_value_by_key(self, key: str) -> object:
        """Retrieves a value from the dispatcher using the provided key."""
        return self.dispatcher.get_value(key)


