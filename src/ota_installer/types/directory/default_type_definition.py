# src/ota_installer/types/directory/default_type_definition.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import types
from typing import cast

from ...images.boot_image.containers.boot_image_container import (
    BootImageContainer,
)
from ...images.magisk_image.constants.magisk_image_paths import (
    MagiskImagePaths,
)
from ...images.magisk_image.containers.magisk_image_container import (
    MagiskImageContainer,
)

magisk_struct = MagiskImageContainer()


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
    magisk_image: Path | MagiskImageContainer = field(
        default_factory=MagiskImageContainer
    )

    def __post_init__(self) -> None:
        self.boot_image = create_structure(
            BootImageContainer, self.boot_image_file_name
        )
        self.magisk_image = create_structure(MagiskImageContainer)


def create_structure[R, **P](
    structure_cls: R, *args: P.args, **kwargs: P.kwargs
) -> R:
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
