# src/ota_installer/image/generic_image_info.py
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..plugin.plugin_registry import dispatcher_plugin


# containers
@dataclass(frozen=True, slots=True)
class FileImagePaths:
    """Represents file and directory paths for a file image."""

    file_path: Path
    directory_path: Path


@dataclass(frozen=True, slots=True)
class FileImageData:
    """Contains information about the file image data."""

    device: str
    build_id: str

    def __call__(self, image: FileImageName | str) -> Path:
        if isinstance(image, FileImageName):
            return image.path(self.device, self.build_id)

        return FileImageName[image.upper()].path(
            self.device,
            self.build_id,
        )


@dataclass(frozen=True, slots=True)
class FileImageInfo:
    directory: Path
    title: str
    extension: str

    def path(self, device: str, build_id: str) -> Path:
        return (
            self.directory
            / f"{device}-{self.title}-{build_id}.{self.extension}"
        )


# enums
class FileImageName(Enum):
    PAYLOAD = FileImageInfo(Path.home(), "payload", "bin")
    STOCK = FileImageInfo(
        Path.home() / "Android" / "boot-images" / "stock",
        "boot",
        "img",
    )
    MAGISK = FileImageInfo(
        Path.home() / "Android" / "boot-images" / "magisk",
        "magisk",
        "img",
    )

    def path(self, device: str, build_id: str) -> Path:
        return self.value.path(device, build_id)

    @property
    def directory(self) -> Path:
        return self.value.directory

    @classmethod
    def path_list(cls) -> tuple[Path, ...]:
        return tuple(member.directory for member in cls)

    @classmethod
    def boot_directories(cls) -> dict[str, Path]:
        return {
            cls.STOCK.name.lower(): cls.STOCK.directory,
            cls.MAGISK.name.lower(): cls.MAGISK.directory,
        }

    def fetch_directory_path(self) -> Path:
        return self.directory

    @classmethod
    def create_path_dictionary(cls, file_paths) -> dict[str, Path]:
        """Compatibility helper for FileImageHandler collection building."""
        return {
            member.name.lower(): getattr(file_paths, member.name.lower())
            for member in cls
        }


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
        self.collection = FileImageName.create_path_dictionary(
            self.obj.file_paths
        )
