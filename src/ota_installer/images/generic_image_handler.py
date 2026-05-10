# images/generic_image_handler.py
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto
from pathlib import Path
from typing import NamedTuple, Self

from ..dispatchers.dispatcher_handler import DispatcherTemplate
from ..dispatchers.dispatcher_type import DispatcherType
from ..dispatchers.plugins.dispatcher_plugin_registry import dispatcher_plugin


# containers
@dataclass(frozen=True, slots=True)
class FileImagePaths(object):
    """Represents file and directory paths for a file image."""

    file_path: Path
    directory_path: Path


class FileImageData(NamedTuple):
    """Contains information about the file image data."""

    device: str
    version: str


# enums
class FileImageNames(StrEnum):
    """Enumeration for File Image Names."""

    STOCK = auto()
    PAYLOAD = auto()
    MAGISK = auto()

    @classmethod
    def create_path_dictionary(cls, file_paths) -> dict[str, str]:
        """create the dictionary with enum member names and their
        corresponding values.
        """
        return {
            enum_member: getattr(file_paths, enum_member)
            for enum_member in cls
        }


class FileImageAttributes(Enum):
    """
    Enumeration to describe file image attributes with associated metadata.
    """

    PAYLOAD = (FileImageNames.PAYLOAD.value, "bin")
    STOCK = ("boot", "img")
    MAGISK = (FileImageNames.MAGISK.value, "img")

    def __init__(self, title: str, extension: str):
        self.title = title
        self.extension = extension
        self.device = ""
        self.build_id = ""

    @property
    def file_name(self) -> str:
        """Generates the formatted file name based on attributes."""

        return f"{self.device}-{self.title}-{self.build_id}.{self.extension}"

    def set_device(self, device: str) -> Self:
        """Sets the device attribute and returns the enum instance."""

        self.device = str(device)
        return self

    def set_version(self, build_id: str) -> Self:
        """Sets the version attribute and returns the enum instance."""

        self.build_id = str(build_id)
        return self

    def set_file_path(self) -> Path:
        """Constructs the full file path for the image file."""
        from .boot_image_handler import BootImagePaths

        boot_image_path = BootImagePaths[self.name].value
        return Path(boot_image_path) / self.file_name


# dispatcher
@dispatcher_plugin(DispatcherType.FILE.value)
@dataclass
class FileTypeDispatcher(DispatcherTemplate):
    """
    Dispatcher for handling file types based on a collection of file paths.
    """

    obj: type = field(default_factory=lambda: type)
    collection: Mapping = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """
        Initializes the collection with normalized keys and corresponding
        file paths.
        """
        self.collection = FileImageNames.create_path_dictionary(
            self.obj.file_paths
        )


# Signed off by Brian Sanford on 20260508
