# src/ota_installer/images/magisk_image/containers/magisk.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.magisk_image_paths import MagiskImagePath
from .magisk_image_tuple import MagiskImageTuple


@dataclass
class MagiskImageContainer(object):
    """Container for managing Magisk image paths."""

    magisk_path: tuple = MagiskImagePath.list()

    @property
    def _path_container(self) -> MagiskImageTuple:
        """Returns a MagiskImageTuple containing local and remote paths."""
        return MagiskImageTuple(*self.magisk_path)

    @property
    def local_path(self) -> Path:
        """Returns the local path from the path container."""
        return self._path_container.local_path

    @property
    def remote_path(self) -> Path:
        """Returns the remote path from the path container."""
        return self._path_container.remote_path


