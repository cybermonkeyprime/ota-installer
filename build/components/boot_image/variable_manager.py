from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from build.components.boot_image.types import (
    BootImageTypeDefinition,
    BootImageTypeManager,
)
from build.components.file.structures import FileNameParserStructure


@dataclass
class BootImageVariableManager(object):
    """Manages boot images by providing file path and related operations.

    Attributes:
        file_path: The path to the boot image file.
    """

    file_path: Path = field(
        default_factory=lambda: Path.home() / "Android" / "boot-images"
    )

    @property
    def parsed_file_name(self) -> FileNameParserStructure:
        """Creates a FileNameParser instance for the boot image file."""
        return FileNameParserStructure(self.file_path.stem)

    @property
    def image_structure(self) -> Optional[BootImageTypeDefinition]:
        """Attempts to create an ImageFile structure for the boot image."""
        file_manager = BootImageTypeManager(self.parsed_file_name, "Android")
        try:
            return file_manager.create_image()
        except Exception as e:
            print(f"Error creating image file: {e}")
            return None

    @property
    def struct(self) -> Optional[BootImageTypeDefinition]:
        """Attempts to create an ImageFile structure for the boot image."""
        return self.image_structure


def main():
    # Example usage
    boot_image_manager = BootImageVariableManager()
    print(boot_image_manager.image_structure)


if __name__ == "__main__":
    main()
