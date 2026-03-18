# src/directories/constants/magisk_paths.py
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MagiskImageContainer(object):
    """Represents a Magisk image with local and remote paths."""

    local_path: Path
    remote_path: Path


class MagiskImagePath(Enum):
    """Enumeration for Magisk image paths."""

    LOCAL_PATH = Path.home() / "Android" / "boot-images" / "magisk"
    REMOTE_PATH = Path("/sdcard") / "Download" / "magisk"

    @classmethod
    def list(cls) -> tuple:
        return tuple(enum_member.value for enum_member in cls)

    @property
    def _path_container(self) -> MagiskImageContainer:
        """Returns a MagiskImageTuple containing local and remote paths."""
        return MagiskImageContainer(*self.list())

    @property
    def local_path(self) -> Path:
        """Returns the local path from the path container."""
        return self._path_container.local_path

    @property
    def remote_path(self) -> Path:
        """Returns the remote path from the path container."""
        return self._path_container.remote_path
