from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BootImageDirectoryStructure:
    parent_directory: str = field(default="")

    boot_image_path: Path = field(default=Path.home() / "Android"/ "boot-images")

    @property
    def stock(self) -> Path:
        return Path.joinpath(self.boot_image_path / "stock")

    @property
    def magisk(self) -> Path:
        return Path.joinpath(self.boot_image_path / "magisk")
