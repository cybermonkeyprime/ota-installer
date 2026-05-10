# directory_handler.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path
from typing import Self

from .dispatchers.dispatcher_template import DispatcherTemplate
from .dispatchers.dispatcher_type import DispatcherType
from .dispatchers.plugins.dispatcher_plugin_registry import dispatcher_plugin
from .display.variables.processors.base_processor import BaseProcessor
from .images.boot_image_handler import (
    BootImageContainer,
    BootImagePaths,
)
from .images.magisk_image.constants.magisk_image_paths import (
    MagiskImageContainer,
)
from .log_setup import logger


# Enums
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


class DirectoryItemType(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str

    @classmethod
    def get_validated_type(cls, field_name: str) -> type:
        """
        Validates field existence using a whitelist check.
        Raises AttributeError immediately on failure (Fail-Fast).
        """
        key = field_name.upper()

        # Explicit membership check: 'Look Before You Leap'
        if not key:
            raise AttributeError(
                f"Invalid field: '{field_name}'. "
                f"Allowed fields are: {', '.join(cls._member_names_)}"
            ) from None

        return cls[field_name.upper()].value


# classes
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


@dataclass
class DirectoryIterationProcessor(BaseProcessor):
    """Processes directory iterations for variable management."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    directory_names: tuple = field(init=False)
    directory_type: str = field(init=False)
    variable_prefix: str = field(init=False)

    def __post_init__(self):
        """Initializes the dispatcher type."""
        self.dispatcher_type = DispatcherType.DIRECTORY.value
        super().__post_init__()

    def set_directory_names(self, directory_names: tuple[str, ...]) -> Self:
        """Sets the directory names for processing."""
        self.directory_names = tuple(directory_names)
        return self

    def set_directory_type(self, directory_type: str) -> Self:
        """Sets the type of directories being processed."""
        self.directory_type = str(directory_type)
        return self

    def set_variable_prefix(self, variable_prefix: str) -> Self:
        """Sets the prefix for variable names."""
        self.variable_prefix = str(variable_prefix)
        return self

    def process_items(self) -> None:
        from .display.variables.classes.variable_table_builder import (
            VariableTableBuilder,
        )
        from .display.variables.containers.variable_item import VariableItem

        """Processes each directory and builds a variable table."""
        builder = VariableTableBuilder(indent=3)
        for directory in self.directory_names:
            title_string = (
                f"{self.directory_type}"
                f"{self.variable_prefix}"
                f"{directory}_directory"
            )
            value_string = str(self.get_value_by_key(directory))
            data = VariableItem(title=title_string, value=value_string)
            builder.add(data.title.upper(), data.value)
        builder.render()


# dispatcher
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


# functions
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


# Signed off by Brian Sanford on 20260508
