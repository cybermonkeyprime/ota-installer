from dataclasses import dataclass, field

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..log_setup import logger
from ..plugin.plugin_registry import Plugin
from .directory_type import DirectoryType


@Plugin.DISPATCHER.register(name=DispatcherType.DIRECTORY.value)
@dataclass
class DirectoryDispatcher(DispatcherTemplate):
    """Handles directory operations for the dispatcher."""

    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        """Initializes the directory collection based on provided object."""
        self.collection = DirectoryType.to_dict(self.obj)
        message = (
            "DirectoryDispatcher initialized with collection: "
            f"{self.collection}"
        )
        logger.debug(message)
