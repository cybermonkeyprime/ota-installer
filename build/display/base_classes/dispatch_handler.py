from dataclasses import dataclass, field

from build.dispatchers import DispatcherManager

import build.variables as variables


@dataclass
class DispatchHandler(object):
    """Handles the creation of dispatchers based on type and variables."""

    dispatcher_type: str = field(default="")
    process_variable: type = field(default_factory=lambda: variables.VariableManager)

    def create_dispatcher(self) -> DispatcherManager:
        return DispatcherManager(self.dispatcher_type, self.process_variable)

    def __str__(self) -> str:
        return str(self.create_dispatcher())
