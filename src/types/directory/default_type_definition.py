from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TypeVar

import src.structures as structures
from src.paths.constants.magisk_image_paths import MagiskImagePaths

magisk_struct = structures.MagiskStruct()

T = TypeVar("T", structures.BootImageStruct, structures.MagiskStruct)


class BootImageTypes(Enum):
    STOCK = "stock"
    MAGISK = "magisk"

    def path(self, parent_directory: Path) -> Path:
        return parent_directory / self.value


@dataclass
class BootImage(object):
    parent_directory: Path = field(default_factory=Path)

    @property
    def stock_image_path(self) -> Path:
        return BootImageTypes.STOCK.path(self.parent_directory)

    @property
    def patched_image_path(self) -> Path:
        return BootImageTypes.MAGISK.path(self.parent_directory)


@dataclass
class DefaultTypeDefinition(object):
    parent_directory: Path
    boot_image_file_name: str = field(default="")
    magisk_image: Path | structures.MagiskStruct = field(
        default_factory=structures.MagiskStruct
    )

    def __post_init__(self) -> None:
        self.boot_image = self.create_structure(
            structures.BootImageStruct, self.boot_image_file_name
        )
        self.magisk_image = self.create_structure(structures.MagiskStruct)

    def create_structure(self, structure_cls: type[T], *args, **kwargs) -> T:
        try:
            return structure_cls(*args, **kwargs)
        except Exception as e:
            raise ValueError("Failed to create structure: ") from e


def main() -> None:
    # Example usage:
    boot_image = BootImage()
    magisk_image = MagiskImagePaths

    print(f"Stock image path: {boot_image.stock_image_path}")
    print(f"Patched image path: {boot_image.patched_image_path}")
    print(f"Magisk local path: {magisk_image.LOCAL_PATH.value}")
    print(f"Magisk remote path: {magisk_image.REMOTE_PATH.value}")


if __name__ == "__main__":
    main()
