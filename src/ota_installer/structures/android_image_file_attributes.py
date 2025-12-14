# src/ota_installer/structures/android_image_file_attributes.py
from dataclasses import dataclass, field


@dataclass
class AndroidImageFileAttributes(object):
    name: str = field(default="")
    extension: str = field(default="")
