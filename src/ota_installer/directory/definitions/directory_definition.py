# src/ota_installer/types/directory/default_type_definition.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from ota_installer.images.boot_image.constants.boot_image_paths import (
    BootImagePaths,
)

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

T = TypeVar("T", bound=type)
# P = ParamSpec("P")


@dataclass
class DirectoryDefinition(object):
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


def create_structure[**P](
    structure_cls: type, *args: P.args, **kwargs: P.kwargs
) -> Callable[P, type]:
    try:
        return structure_cls(*args, **kwargs)
    except Exception as err:
        raise ValueError("Failed to create structure: ") from err


def main() -> None:
    # Example usage:
    boot_image = BootImagePaths
    magisk_image = MagiskImagePaths

    print(f"Stock image path: {boot_image.STOCK.value}")
    print(f"Patched image path: {boot_image.MAGISK.value}")
    print(f"Magisk local path: {magisk_image.LOCAL_PATH.value}")
    print(f"Magisk remote path: {magisk_image.REMOTE_PATH.value}")


if __name__ == "__main__":
    main()
