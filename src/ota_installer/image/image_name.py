from enum import Enum
from pathlib import Path

from ..variable.variable_info import FilePathRenderer
from .image_containers import ImageRenderer


class ImageName(Enum):
    PAYLOAD = ImageRenderer(Path.home(), "payload", "bin")
    STOCK = ImageRenderer(
        Path.home() / "Android" / "boot-images" / "stock",
        "boot",
        "img",
    )
    MAGISK = ImageRenderer(
        Path.home() / "Android" / "boot-images" / "magisk",
        "magisk",
        "img",
    )

    @classmethod
    def valid_members(cls) -> tuple:
        return tuple(member.name for member in cls)

    def path(self, device: str, build_id: str) -> Path:
        return self.value.path(device, build_id)

    @property
    def directory(self) -> Path:
        return self.value.directory

    @classmethod
    def path_list(cls) -> tuple[Path, ...]:
        return tuple(member.directory for member in cls)

    @classmethod
    def boot_directories(cls) -> dict[str, Path]:
        return {
            cls.STOCK.name.lower(): cls.STOCK.directory,
            cls.MAGISK.name.lower(): cls.MAGISK.directory,
        }

    def fetch_directory_path(self) -> Path:
        return self.directory

    @classmethod
    def create_path_dictionary(
        cls, file_paths: FilePathRenderer
    ) -> dict[str, Path]:
        """Build a mapping of image names to their generated paths."""
        return {
            member.name.lower(): getattr(file_paths, member.name.lower())
            for member in cls
        }
