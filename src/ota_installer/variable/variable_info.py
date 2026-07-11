# variables/variable_info.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..plugin.plugin_registry import dispatcher_plugin

T = TypeVar("T")

StrPathDict = dict[str, Path | str]


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class DirectoryNames:
    """Container for directory names used in the OTA installer."""

    magisk: DirectoryPaths

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass(frozen=True, slots=True)
class FileNameInfo:
    """Represents information about a file name."""

    path: Path
    stem: str
    parts: FileNameContainer
    device: str
    version: str


@dataclass(frozen=True, slots=True)
class FilePaths:
    """Container for file paths used in the OTA installer."""

    stock: Path
    magisk: Path
    payload: Path
    log_file: str

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass(frozen=True, slots=True)
class FileNameContainer:
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None

    @property
    def log_file(self) -> str:
        """Generate a log file path based on device and version."""
        return f"/tmp/ota-installer_{self.device}_{self.build_id}.txt"

    @property
    def image_data(self):
        from ..image.generic_image_info import FileImageData

        return FileImageData(self.device, self.build_id)

    def create_image(self, image):
        return self.image_data(image)


@dataclass(frozen=True, slots=True)
class VariableContext:
    """Container for variable types used in OTA installation."""

    file_path: Path
    magisk_image_name: str
    file_path_stem: str
    file_parts: FileNameContainer


@dataclass(frozen=True)
class VariableRenderer(Generic[T]):
    class_type: type[T]

    def __call__(self, **arguments: Any) -> T:
        return self.class_type(**arguments)


class VariableType(Enum):
    CONTEXT = VariableRenderer(VariableContext)
    FILE_NAME = VariableRenderer(FileNameInfo)
    FILE_PATH = VariableRenderer(FilePaths)
    DIRECTORY = VariableRenderer(DirectoryNames)

    def build(self, **kwargs: Any) -> Any:
        return self.value(**kwargs)


@dispatcher_plugin(name=DispatcherType.VARIABLE.value)
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


# Signed off by Brian Sanford on 20260625
