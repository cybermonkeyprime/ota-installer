# src/ota_installer/images/file_image/containers/file_image_container.py
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple


@dataclass(frozen=True, slots=True)
class FileImagePaths(object):
    """Represents file and directory paths for a file image."""

    file_path: Path
    directory_path: Path


class FileImageData(NamedTuple):
    """Contains information about the file image data."""

    device: str
    version: str


# Signed off by Brian Sanford on 20260317
