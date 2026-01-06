# src/ota_installer/types/directory/default_type_definition.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

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


@dataclass
class DirectoryTypeDefinition(object):
    parent_directory: Path
    _boot_image: str = field(default="")
    magisk_image: Path | MagiskImageContainer = field(
        default_factory=MagiskImageContainer
    )

    def __post_init__(self) -> None:
        self.boot_image = create_container(
            BootImageContainer, self._boot_image
        )
        self.magisk_image = create_container(MagiskImageContainer)


def create_container[R, **P](
    container_cls: R, *args: P.args, **kwargs: P.kwargs
) -> Callable[P, R]:
    try:
        logger.debug(f"{type(container_cls).__name__} {args}")
        return container_cls(*args, **kwargs)
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
