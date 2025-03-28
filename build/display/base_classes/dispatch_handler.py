from dataclasses import dataclass, field

from build.dispatchers import MainDispatcher

import build.variables as variables

VariableManager = variables.VariableManager


@dataclass
class DispatchHandler(object):
    """Handles the creation of dispatchers based on type and variables."""

    dispatcher_type: str = field(default="")
    process_variable: VariableManager = field(default_factory=VariableManager)

    def create_dispatcher(self) -> MainDispatcher:
        return MainDispatcher(self.dispatcher_type, self.process_variable)

    def __str__(self) -> str:
        return str(self.create_dispatcher())
