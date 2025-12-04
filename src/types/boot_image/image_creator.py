# src/types/boot_image/image_creator.py
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from logger import logger


class DirectoryPaths(Enum):
    PAYLOAD = Path.home()
    BOOT = Path.home() / "Android" / "boot-images" / "stock"
    MAGISK = Path.home() / "Android" / "boot-images" / "magisk"


# Core image creation utility
@dataclass
class ImageCreator(object):
    def set_device(self, device: str):
        self.device = str(device)
        return self

    def set_version(self, version: str):
        self.version = str(version)
        return self

    def set_file_name(self, file_name: str):
        self.file_type = str(file_name)
        return self

    def set_extension(self, extension: str):
        self.extension = str(extension)
        return self

    def set_path(self, path: str):
        self.path = str(path)
        return self

    def set_directory_path(self, directory_path: Path):
        self.directory_path = Path(directory_path)
        return self

    def generate_file_name(self) -> str | None:
        file_name = (
            f"{self.device}-{self.file_type}-{self.version}.{self.extension}"
        )
        try:
            return (
                f"{DirectoryPaths[self.file_type.upper()].value}/{file_name}"
            )
        except Exception as err:
            logger.error(f"[Error] ImageCreator: {err}")

    def generate_directory(self) -> str:
        return f"{self.path}" or ""
