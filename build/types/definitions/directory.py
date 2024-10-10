from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Type

import build.structures as structures

magisk_instance = structures.MagiskStruct()


@dataclass
class BootImage:
    parent_directory: Path = field(default_factory=Path)
    stock_image_path: Path = field(init=False)
    patched_image_path: Path = field(init=False)

    def __post_init__(self) -> None:
        self.stock_image_path = Path(f"{self.parent_directory}/stock")
        self.patched_image_path = Path(f"{self.parent_directory}/magisk")


@dataclass
class MagiskImage:
    local_path: Path = field(default_factory=lambda: Path(magisk_instance.local_path))
    remote_path: Path = field(default_factory=lambda: Path(magisk_instance.remote_path))


@dataclass
class Directory:
    parent_directory: Path
    boot_image_file_name: str = field(default="")
    magisk_image: structures.MagiskStruct = field(
        default_factory=structures.MagiskStruct
    )

    def __post_init__(self) -> None:
        self.boot_image = self.create_structure(
            structures.BootImageStruct, self.boot_image_file_name
        )
        self.magisk_image = self.create_structure(structures.MagiskStruct)

    def create_structure(self, structure_cls: Type[Any], *args, **kwargs) -> Any:
        try:
            return structure_cls(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create structure: {e}")


def main() -> None:
    # Example usage:
    directory_manager = Directory(
        parent_directory=Path("/path/to/directory"), boot_image_file_name="boot.img"
    )
    print(f"Stock image path: {directory_manager.boot_image.stock_image_path}")
    print(f"Patched image path: {directory_manager.boot_image.patched_image_path}")
    print(f"Magisk local path: {directory_manager.magisk_image.local_path}")
    print(f"Magisk remote path: {directory_manager.magisk_image.remote_path}")


if __name__ == "__main__":
    main()
