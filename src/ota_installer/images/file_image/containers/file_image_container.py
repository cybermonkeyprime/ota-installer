# src/ota_installer/images/file_image/containers/file_image_container.py
from pathlib import Path
from typing import NamedTuple


class FileImagePaths(NamedTuple):
    """Represents file and directory paths for a file image."""

    file_path: Path
    directory_path: Path


class FileImageData(NamedTuple):
    """Contains information about the file image data."""

    device: str
    version: str


class FileImageStruct(NamedTuple):
    """Defines the structure of a file image with title and extension."""

    title: str
    extension: str


# may change to dataclass in future

# Signed off by Brian Sanford on 20260129
