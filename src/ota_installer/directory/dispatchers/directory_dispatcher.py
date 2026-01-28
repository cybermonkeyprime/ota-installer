# src/ota_installer/directory/dispatchers/directory_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

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
        self.collection = self._initialize_collection(boot_image)
        logger.debug(
            f"DirectoryDispatcher initialized with collection: "
            f"{self.collection}"
        )

    def _initialize_collection(self, boot_image: type) -> dict:
        """Creates a directory collection from the boot image."""
        return {
            DirectoryType.STOCK: Path(boot_image.stock),
            DirectoryType.MAGISK: Path(boot_image.magisk),
            DirectoryType.LOCAL: Path(self.obj.directories.magisk.local_path),
            DirectoryType.REMOTE: Path(
                self.obj.directories.magisk.remote_path
            ),
        }


# Signed off by Brian Sanford on 20260127
