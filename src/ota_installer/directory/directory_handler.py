# src/ota_installer/handler/directory_handler.py
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path

from ..dispatcher.dispatcher_handler import DispatcherTemplate
from ..dispatcher.dispatcher_info import DispatcherType
from ..log_setup import logger
from ..plugin.plugin_registry import dispatcher_plugin


# Enums
class DirectoryInfo(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def mapping(cls, obj: Callable) -> Mapping[str, Path]:
        """Creates a directory collection from the boot image."""
        boot_image = obj.directory.boot_image
        magisk_image = obj.directories.magisk
        return {
            cls.STOCK: Path(boot_image.stock),
            cls.MAGISK: Path(boot_image.magisk),
            cls.LOCAL: Path(magisk_image.local_path),
            cls.REMOTE: Path(magisk_image.remote_path),
        }

    def get_key(self, obj) -> Path:
        return self.mapping(obj)[self.value.upper()]


@dataclass
class DirectoryDefinition:
    """
    Defines the structure for a directory containing boot and magisk images.
    """

    parent_directory: Path
    _boot_image: str = field(default="")
    magisk_image: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        from ..image.boot_image_handler import BootImageContainer
        from ..image.magisk_image_handler import MagiskImageContainer

        """
        Initializes the boot image container after the dataclass is created.
        """
        self.boot_image = self._create_container(
            BootImageContainer, self._boot_image
        )
        self.magisk_image_container = self._create_container(
            MagiskImageContainer
        )

    def _create_container(
        self, container_cls: type, *args, **kwargs
    ) -> Callable | None:
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating {container_cls.__name__} with args: {args}")
        return container_cls(*args) if args else None


# dispatcher
@dispatcher_plugin(DispatcherType.DIRECTORY.value)
@dataclass
class DirectoryDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        """
        Initializes the directory collection based on the provided object.
        """
        self.collection = DirectoryInfo.mapping(self.obj)
        logger.debug(
            f"DirectoryDispatcher initialized with collection: "
            f"{self.collection}"
        )


# functions
def set_directory(parent_directory: Path) -> DirectoryDefinition:
    from ..image.boot_image_handler import BootImagePaths

    """Creates a DirectoryTypeDefinition for the specified parent directory."""

    logger.debug("Creating Directories")
    if not parent_directory.exists() or not parent_directory.is_dir():
        message = f"Invalid parent directory: {parent_directory}"
        logger.error(message)
        raise SystemExit(message)

    return DirectoryDefinition(
        parent_directory,
        str(BootImagePaths.STOCK.value),
        BootImagePaths.MAGISK.value,
    )


# Signed off by Brian Sanford on 20260523
