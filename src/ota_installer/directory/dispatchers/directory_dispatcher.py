# src/ota_installer/directory/dispatchers/directory_dispatcher.py
from dataclasses import dataclass, field

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ...dispatchers.templates.dispatcher_template import DispatcherTemplate
from ...log_setup import logger
from ..constants.directory_type import DirectoryType


@dispatcher_plugin(DispatcherConstants.DIRECTORY.value)
@dataclass
class DirectoryDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        """
        Initializes the directory collection based on the provided object.
        """
        self.collection = DirectoryType.mapping(self.obj)
        logger.debug(
            f"DirectoryDispatcher initialized with collection: "
            f"{self.collection}"
        )


# Signed off by Brian Sanford on 20260410
