# src/ota_installer/images/boot_image/containers/boot_image_conatiner.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.boot_image_paths import BootImagePaths


@dataclass
class BootImageContainer(object):
    path_list = [enum_member.value for enum_member in BootImagePaths]
    stock: Path = BootImagePaths.STOCK.value

    magisk: Path = BootImagePaths.MAGISK.value
