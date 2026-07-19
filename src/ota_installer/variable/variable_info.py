# src/ota_installer/variable/variable_info.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

from ota_installer.image.generic_image_info import FileImageName

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..plugin.plugin_registry import Plugin

T = TypeVar("T")

StrPathDict = dict[str, Path | str]


@dataclass(frozen=False, slots=True)
class MagiskPathGroup:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class DirectoryNames:
    """Container for directory names used in the OTA installer."""

    magisk: MagiskPathGroup

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass(frozen=True, slots=True)
class FileNameInfo:
    """Represents information about a file name."""

    path: Path
    parts: FilePathRenderer

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def device(self) -> str:
        return self.parts.device

    @property
    def version(self) -> str:
        return self.parts.build_id


@dataclass(frozen=True, slots=True)
class FilePathRenderer:
    """Container for file paths used in the OTA installer."""

    device: str
    build_id: str

    def __iter__(self):
        return iter(self.__dict__.items())

    @property
    def image_data(self) -> "FileImageData":
        from ..image.generic_image_info import FileImageData

        return FileImageData(self.device, self.build_id)

    @property
    def stock(self) -> str:
        return self.create_image(FileImageName.STOCK)

    @property
    def magisk(self) -> str:
        return self.create_image(FileImageName.MAGISK)

    @property
    def payload(self) -> str:
        return self.create_image(FileImageName.PAYLOAD)

    @property
    def log_file(self) -> Path:
        """Generate a log file path based on device and version."""
        from tempfile import gettempdir

        return (
            Path(gettempdir())
            / f"ota-installer_{self.device}_{self.build_id}.txt"
        )

    @property
    def magisk_image_name(self) -> str:
        return "place_holder"

    def create_image(self, image):
        return self.image_data(image)


@dataclass(frozen=True, slots=True)
class FilePartContainer:
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


@dataclass(frozen=True, slots=True)
class FilePartRenderer:
    """Container for variable types used in OTA installation."""

    file_path: Path

    @property
    def file_path_stem(self):
        return self.file_path.stem

    @property
    def file_parts(self) -> FilePartContainer:
        """Parse the raw file name into its components."""
        from parse import parse

        FILE_PATTERN = "{device}-{pkg_type}-{build_id}-{signature}"
        result = parse(FILE_PATTERN, self.file_path.stem)
        if result is None:
            message = f"Invalid OTA filename: {self.file_path_stem!r}"
            raise ValueError(message)

        return FilePartContainer(**result.named)


@dataclass(frozen=True)
class VariableRenderer(Generic[T]):
    class_type: type[T]

    def __call__(self, **arguments: Any) -> T:
        return self.class_type(**arguments)


class VariableType(Enum):
    CONTEXT = VariableRenderer(FilePartRenderer)
    FILE_NAME = VariableRenderer(FileNameInfo)
    FILE_PATH = VariableRenderer(FilePathRenderer)
    DIRECTORY = VariableRenderer(DirectoryNames)

    def build(self, **kwargs: Any) -> Any:
        return self.value(**kwargs)


@Plugin.DISPATCHER.register(name=DispatcherType.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling variable types."""

    obj: type = field(default_factory=lambda: type)
    collection: StrPathDict = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the collection of paths based on the provided object."""
        self.collection = self._initialize_collection()

    def _initialize_collection(self) -> StrPathDict:
        """Creates a collection of paths and log file."""
        return {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths.log_file,
        }


# Signed off by Brian Sanford on 20260712
