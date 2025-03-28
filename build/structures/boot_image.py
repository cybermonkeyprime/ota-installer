from dataclasses import dataclass
from pathlib import Path


@dataclass
class BootImage:
    parent_directory: str

    @property
    def stock(self) -> Path:
        return Path.home() / self.parent_directory / "stock"

    @property
    def magisk(self) -> Path:
        return Path.home() / self.parent_directory / "magisk"

    def __str__(self) -> str:
        return self.parent_directory
