# src/ota_installer/handler/directory_info.py
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..log_setup import logger
from ..plugin.plugin_registry import Plugin


# Enums
class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def from_object(cls, data: "VariableDirector") -> dict[Enum, Path]:
        """Creates a directory collection from the boot image."""
        boot_image = data.directory.boot_image
        magisk_image = data.directories.magisk

        boot_dict = {
            cls[name.upper()]: getattr(boot_image, name)
            for name in ["stock", "magisk"]
        }
        magisk_dict = {
            cls[name.upper()]: Path(getattr(magisk_image, f"{name}_path"))
            for name in ["local", "remote"]
        }

        return {**boot_dict, **magisk_dict}

    def get_path(self, obj) -> Path:
        return self.from_object(obj)[self]


class DirectoryRender(Enum):
    from ..image.boot_image_info import BootImageContainer
    from ..image.magisk_image_info import MagiskImageContainer

    BOOT = BootImageContainer.create
    MAGISK = MagiskImageContainer

    def __call__(self, *args, **kwargs):
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating directory container: {self.name}")
        return self.value(*args) if args else None


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
        self.boot_image = DirectoryRender.BOOT()
        self.magisk_image_container = DirectoryRender.MAGISK("", "")


# dispatcher
@Plugin.DISPATCHER.register(name=DispatcherType.DIRECTORY.value)
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
    from ..image.generic_image_info import FileImageName

    logger.debug("Creating Directories")
    if not parent_directory.exists() or not parent_directory.is_dir():
        message = f"Invalid parent directory: {parent_directory}"
        logger.error(message)
        raise SystemExit(message)

    return DirectoryConfig(
        parent_directory,
        (FileImageName.STOCK.fetch_directory_path()),
        FileImageName.MAGISK.fetch_directory_path(),
    )


# Signed off by Brian Sanford on 20260626
