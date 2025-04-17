from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from build.components.directory.structures import (
    BootImageDirectoryStructure,
    MagiskImageDirectoryStructure,
)


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
    def boot_image_path(self) -> Any:
        return self.create_structure(
            BootImageDirectoryStructure, self.boot_image_file_name
        )

    def create_structure(
        self, structure_cls: Callable, *args: Any, **kwargs: Any
    ) -> Any:
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
    print(f"Stock image path: {directory_manager.boot_image_path.stock_image_path}")
    print(f"Patched image path: {directory_manager.boot_image_path.patched_image_path}")
    print(f"Magisk local path: {directory_manager.magisk_image.local_path}")
    print(f"Magisk remote path: {directory_manager.magisk_image.remote_path}")
    return True


if __name__ == "__main__":
    main()
