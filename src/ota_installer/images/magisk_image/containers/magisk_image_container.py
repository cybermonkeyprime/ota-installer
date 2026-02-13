# src/ota_installer/images/magisk_image/containers/magisk.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.magisk_image_paths import MagiskImagePaths
from .magisk_image_tuple import MagiskImageTuple


@dataclass
class MagiskImageContainer(object):
    """Container for managing Magisk image paths."""

    @property
    def path_data(self) -> list:
        """
        Returns a list of path values from the Magisk image paths enumeration.
        """
        return [enum_member.value for enum_member in MagiskImagePaths]

    @property
    def path_container(self) -> MagiskImageTuple:
        """Returns a MagiskImageTuple containing local and remote paths."""
        return MagiskImageTuple(*self.path_data)

    @property
    def local_path(self) -> Path:
        """Returns the local path from the path container."""
        return self.path_container.local_path

    @property
    def remote_path(self) -> Path:
        """Returns the remote path from the path container."""
        return self.path_container.remote_path


# Signed off by Brian Sanford on 20260213
