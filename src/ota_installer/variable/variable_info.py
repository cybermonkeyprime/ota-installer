# variables/variable_info.py
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class DirectoryNames:
    """Container for directory names used in the OTA installer."""

    magisk: DirectoryPaths


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


@dataclass(frozen=True, slots=True)
class FileNameContainer:
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


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


# Signed off by Brian Sanford on 20260509
