# variables/variable_info.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DirectoryNames(object):
    """Container for directory names used in the OTA installer."""

    magisk: "DirectoryPaths"


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class FileNameInfo(object):
    """Represents information about a file name."""

    path: Path
    stem: str
    parts: "FileNameContainer"
    device: str
    version: str


@dataclass(frozen=True, slots=True)
class FilePaths(object):
    """Container for file paths used in the OTA installer."""

    stock: Path
    magisk: Path
    payload: Path
    log_file: str


@dataclass(frozen=True, slots=True)
class FileNameContainer(object):
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


@dataclass(frozen=True, slots=True)
class VariableTypeContainer(object):
    """Container for variable types used in OTA installation."""

    file_path: Path
    magisk_image_name: str
    file_path_stem: str
    file_parts: FileNameContainer


# Signed off by Brian Sanford on 20260509
