# src/ota_installer/handler/directory_handler.py
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path

from ..dispatcher.dispatcher_handler import DispatcherTemplate
from ..dispatcher.dispatcher_info import DispatcherType
from ..log_setup import logger
from ..plugin.plugin_registry import dispatcher_plugin


# Enums
class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def from_object(cls, obj: "VariableManager") -> Mapping[str, Path]:
        """Creates a directory collection from the boot image."""
        boot_image = obj.directory.boot_image
        magisk_image = obj.directories.magisk
        return {
            cls.STOCK: Path(boot_image.stock),
            cls.MAGISK: Path(boot_image.magisk),
            cls.LOCAL: Path(magisk_image.local_path),
            cls.REMOTE: Path(magisk_image.remote_path),
        }

    def get_path(self, obj) -> Path:
        return self.from_object(obj)[self.value.upper()]


class DirectoryRender(Enum):
    from ..image.boot_image_handler import BootImageContainer
    from ..image.magisk_image_handler import MagiskImageContainer

    BOOT = BootImageContainer
    MAGISK = MagiskImageContainer

    @property
    def container(self):
        return self.value

    def __call__(self, *args, **kwargs):
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating {self.container.__name__} with args: {args}")
        return self.container(*args) if args else None


@dataclass
class DirectoryConfig:
    """
    Defines the structure for a directory containing boot and magisk images.
    """

    parent_directory: Path
    _boot_image: Path = field(default_factory=Path)
    magisk_image: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        """
        Initializes the boot image container after the dataclass is created.
        """
        self.boot_image = DirectoryRender.BOOT(self._boot_image)
        self.magisk_image_container = DirectoryRender.MAGISK("", "")


# dispatcher
@dispatcher_plugin(DispatcherType.DIRECTORY.value)
@dataclass
class DirectoryHandler(DispatcherTemplate):
    """Handles directory operations for the dispatcher."""

    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        """Initializes the directory collection based on provided object."""
        self.collection = DirectoryType.from_object(self.obj)
        message = (
            "DirectoryDispatcher initialized with collection: "
            f"{self.collection}"
        )
        logger.debug(message)


# functions
def set_directory(parent_directory: Path) -> DirectoryConfig:
    """Creates a DirectoryTypeDefinition for the specified parent directory."""
    from ..image.boot_image_handler import BootImagePaths

    logger.debug("Creating Directories")
    if not parent_directory.exists() or not parent_directory.is_dir():
        message = f"Invalid parent directory: {parent_directory}"
        logger.error(message)
        raise SystemExit(message)

    return DirectoryConfig(
        parent_directory,
        (BootImagePaths.STOCK.value),
        BootImagePaths.MAGISK.value,
    )


# Signed off by Brian Sanford on 20260523
