# src/ota_installer/variable/variable_info.py
from dataclasses import dataclass
from pathlib import Path

from .file_part_renderer import FilePartContainer


@dataclass(frozen=False, slots=True)
class MagiskPaths:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class DirectoryNames:
    """Container for directory names used in the OTA installer."""

    magisk: MagiskPaths

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass(frozen=True, slots=True)
class FileNameInvocation:
    """Represents information about a file name."""

    path: Path
    parts: FilePartContainer

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def device(self) -> str:
        return self.parts.device


# Signed off by Brian Sanford on 20260712
