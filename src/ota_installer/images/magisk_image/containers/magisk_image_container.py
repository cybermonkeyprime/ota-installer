# src/ota_installer/images/magisk_image/containers/magisk.py
from dataclasses import dataclass

from ..constants.magisk_image_paths import MagiskImagePaths
from .magisk_image_tuple import MagiskImageTuple


@dataclass
class MagiskImageContainer(object):
    @property
    def path_data(self) -> list:
        return [enum_member.value for enum_member in MagiskImagePaths]

    @property
    def path_container(self):
        return MagiskImageTuple(*self.path_data)

    @property
    def local_path(self):
        return self.path_container.local_path

    @property
    def remote_path(self):
        return self.path_container.remote_path
