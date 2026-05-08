# directory_handler.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path

from .dispatchers.constants.dispatcher_type import DispatcherType
from .dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from .dispatchers.templates.dispatcher_template import DispatcherTemplate
from .images.boot_image_handler import (
    BootImageContainer,
    BootImagePaths,
)
from .images.magisk_image.constants.magisk_image_paths import (
    MagiskImageContainer,
)
from .log_setup import logger


class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def mapping(cls, obj: type) -> dict:
        """Creates a directory collection from the boot image."""
        boot_image = obj.directory.boot_image
        magisk_image = obj.directories.magisk
        return {
            cls.STOCK: Path(boot_image.stock),
            cls.MAGISK: Path(boot_image.magisk),
            cls.LOCAL: Path(magisk_image.local_path),
            cls.REMOTE: Path(magisk_image.remote_path),
        }


@dataclass
class DirectoryTypeDefinition(object):
    """
    Defines the structure for a directory containing boot and magisk images.
    """

    parent_directory: Path
    _boot_image: str = field(default="")
    magisk_image: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        """
        Initializes the boot image container after the dataclass is created.
        """
        self.boot_image = self.create_container(
            BootImageContainer, self._boot_image
        )
        self.magisk_image_container = self.create_container(
            MagiskImageContainer
        )

    def create_container(
        self, container_cls: Callable, *args, **kwargs
    ) -> Callable | None:
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating {container_cls.__name__} with args: {args}")
        return container_cls(*args) if args else None


def set_directory(
    parent_directory: Path,
) -> DirectoryTypeDefinition | None:
    """Creates a DirectoryTypeDefinition for the specified parent directory."""

    logger.debug("Creating Directories")
    if not any([parent_directory.exists(), parent_directory.is_dir()]):
        logger.error("Invalid parent directory: %s", parent_directory)
        return None

    return DirectoryTypeDefinition(
        parent_directory,
        str(BootImagePaths.STOCK.value),
        BootImagePaths.MAGISK.value,
    )


@dispatcher_plugin(DispatcherType.DIRECTORY.value)
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


# Signed off by Brian Sanford on 20260508
