from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar
from collections.abc import Callable

from src.components.directories.structures import (
    BootImageDirectoryStructure,
    MagiskImageDirectoryStructure,
)

T = TypeVar("T")


@dataclass
class DirectoryTypeDefinition:
    parent_directory: Path
    boot_image_file_name: str = field(default="")
    magisk_image: MagiskImageDirectoryStructure = field(
        default_factory=MagiskImageDirectoryStructure
    )

    @property
    def magisk_image_path(self) -> Callable:
        return self.create_structure(MagiskImageDirectoryStructure)

    @property
    def boot_image_path(self) -> object:
        return self.create_structure(
            BootImageDirectoryStructure, self.boot_image_file_name
        )

    def create_structure(
        self, structure_cls: Callable, *args: T, **kwargs: T
    ) -> T:
        try:
            return structure_cls(*args, **kwargs)
        except Exception as error:
            raise ValueError("Failed to create structure") from error


def main() -> bool:
    # Example usage:
    directory_manager = DirectoryTypeDefinition(
        parent_directory=Path("/path/to/directory"),
        boot_image_file_name="boot.img",
    )
    print(
        f"Stock image path: {directory_manager.boot_image_path.stock_image_path}"
    )
    print(
        f"Patched image path: {directory_manager.boot_image_path.patched_image_path}"
    )
    print(f"Magisk local path: {directory_manager.magisk_image.local_path}")
    print(f"Magisk remote path: {directory_manager.magisk_image.remote_path}")
    return True


if __name__ == "__main__":
    main()
