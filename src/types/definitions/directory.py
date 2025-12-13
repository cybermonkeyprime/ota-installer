from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import TypeVar

import src.structures as structures
from src.structures import MagiskImageStruct

magisk_instance = structures.MagiskStruct()

T = TypeVar("T")


@dataclass
class _Directory(object):
    parent_directory: Path
    boot_image_file_name: str = field(default="")
    magisk_image: MagiskImageStruct = field(default_factory=MagiskImageStruct)

    def __post_init__(self) -> None:
        self.boot_image = self.create_structure(
            structures.BootImageStruct, self.boot_image_file_name
        )

        self.magisk_image = self.create_structure(MagiskImageStruct)

    def create_structure(self, structure_cls: type[T], *args, **kwargs) -> T:
        try:
            return structure_cls(*args, **kwargs)
        except Exception as err:
            raise ValueError(f"Failed to create structure: {err}") from err


def main() -> None:
    # Example usage:
    directory_manager = _Directory(
        parent_directory=Path("/path/to/directory"),
        boot_image_file_name="boot.img",
    )
    print(f"Stock image path: {directory_manager.boot_image.stock_image_path}")
    print(
        f"Patched image path: {directory_manager.boot_image.patched_image_path}"
    )
    print(f"Magisk local path: {directory_manager.magisk_image.local_path}")
    print(f"Magisk remote path: {directory_manager.magisk_image.remote_path}")


if __name__ == "__main__":
    main()
