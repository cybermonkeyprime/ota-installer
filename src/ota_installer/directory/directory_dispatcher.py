# src/ota_installer/directory/directory_dispatcher.py
from dataclasses import dataclass, field

from ..dispatcher.dispatcher_template import DispatcherTemplate
from ..dispatcher.dispatcher_type import DispatcherType
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


# Signed off by Brian Sanford on 20260827
