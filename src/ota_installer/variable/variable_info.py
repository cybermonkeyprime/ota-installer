# src/ota_installer/variable/variable_info.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

from ..dispatcher.dispatcher_template import DispatcherTemplate
from ..dispatcher.dispatcher_type import DispatcherType
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
    parts: FilePartContainer

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def device(self) -> str:
        return self.parts.device


@dataclass(frozen=True, slots=True)
class FilePathRenderer:
    """Container for file paths used in the OTA installer."""

    parts: FilePartContainer
    stock: str | None = None
    magisk: str | None = None
    payload: str | None = None

    def __iter__(self):
        return iter(self.__dict__.items())

    def __post_init__(self) -> None:
        self.image_pipeline()

    @property
    def magisk_image_name(self) -> str:
        return "place_holder"

    @property
    def image_data(self) -> "FileImageData":
        from ..image.generic.generic_image_info import FileImageData

        return FileImageData(self.parts.device, self.parts.build_id)

    @property
    def log_file(self) -> Path:
        """Generate a log file path based on device and version."""
        from tempfile import gettempdir

        return (
            Path(gettempdir())
            / f"ota-installer_{self.parts.device}_{self.parts.build_id}.txt"
        )

    def image_pipeline(self) -> None:
        from ..image.generic.generic_image_info import FileImageName

        for key in FileImageName.valid_members():
            value = self.image_data(FileImageName[key])
            object.__setattr__(self, key.lower(), value)


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
    def file_parts(self) -> FilePartContainer:
        """Parse the raw file name into its components."""

        from parse import parse

        FILENAME_PATTERN = "{device}-{pkg_type}-{build_id}-{signature}"

        filename_stem = self.file_path.stem

        result = parse(FILENAME_PATTERN, filename_stem)

        if result is None:
            message = f"Invalid OTA filename: {filename_stem!r}"
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
