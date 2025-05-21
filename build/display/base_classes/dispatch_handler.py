from dataclasses import dataclass, field

from build.dispatchers import DispatcherManager
from build.dispatchers.dispatcher_mapper import DispatcherType


@dataclass
class DispatchHandler(object):
    """Handles the creation of dispatchers based on type and variables."""

    dispatcher_type: DispatcherType = field(default=DispatcherType.IMAGE)
    process_variable: type = field(default_factory=lambda: type)

    def create_dispatcher(self) -> DispatcherManager:
        return DispatcherManager(self.dispatcher_type, self.process_variable)

    def __str__(self) -> str:
        return str(self.create_dispatcher())
