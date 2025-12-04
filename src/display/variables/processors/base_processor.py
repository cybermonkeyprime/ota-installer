# src/display/variables/processors/base_processor.py

from dataclasses import dataclass, field

import src.variables as variables
from src.types import DispatcherProtocol


@dataclass
class BaseProcessor(object):
    processing_function: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )
    dispatcher: DispatcherProtocol = field(init=False)
    dispatcher_type: str | None = None  # To be set in subclasses

    def __post_init__(self):
        if not self.dispatcher_type:
            raise ValueError(
                "dispatcher_type must be set in subclass before __post_init__"
            )
        self.dispatcher = self.processing_function.get_dispatcher(
            self.dispatcher_type
        )

    def get_value_by_key(self, key: str) -> object:
        return self.dispatcher.get_value(key)
