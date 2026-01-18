# src/ota_installer/directory/dispatchers/directory_dispatcher.py
from dataclasses import dataclass, field

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ...dispatchers.templates.dispatcher_template import DispatcherTemplate
from ...log_setup import logger
from ..constants.directory_type import DirectoryType

DIRECTORY = DirectoryType


@dispatcher_plugin(DispatcherConstants.DIRECTORY.value)
@dataclass
class DirectoryDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        """
        Initializes the directory collection based on the provided object.
        """
        boot_image = self.obj.directory.boot_image
        self.collection = {
            DIRECTORY.STOCK: boot_image.stock,  # stock_path
            DIRECTORY.MAGISK: boot_image.magisk,  # magisk_path
            DIRECTORY.LOCAL: self.obj.directories.magisk.local_path,
            DIRECTORY.REMOTE: self.obj.directories.magisk.remote_path,
        }
        logger.debug(
            f"DirectoryDispatcher.__post_init__(): {self.collection=}"
        )


# Signed off by Brian Sanford on 20260117
