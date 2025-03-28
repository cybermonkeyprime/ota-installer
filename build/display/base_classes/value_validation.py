from dataclasses import dataclass, field

from dispatchers import MainDispatcher

import build.variables as variables
from build.dispatchers.dispatcher_template import (
    CollectionDictionary,
    DispatcherTemplate,
)

VariableManager = variables.VariableManager


@dataclass
class ValueValidation(object):
    """Validates values using a dispatch handler."""

    dispatch_handler: MainDispatcher = field(default_factory=MainDispatcher)

    def fetcher(self) -> DispatcherTemplate:
        return self.dispatch_handler.receiver()

    def validate_value(self, key: str) -> CollectionDictionary:
        value = self.fetcher().get_value(key=key)
        value = self.dispatch_handler.receiver().get_value(key=key)
        if value is None:
            print(f"{value=}")
        return value
