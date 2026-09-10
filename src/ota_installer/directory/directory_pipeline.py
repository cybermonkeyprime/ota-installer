# src/ota_installer/directory/directory_pipeline.py
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from ..log_setup import log_status
from .directory_renderer import DirectoryRender


@dataclass
class DirectoryPipeline:
    """
    Defines the structure for a directory containing boot and magisk images.
    """

    @property
    def valid_keys(self) -> tuple[str, ...]:
        return ("parent_directory", "_boot_image", "magisk_image")

    def __post_init__(self) -> None:
        """
        Initializes the boot image container after the dataclass is created.
        """
        self.boot_image = DirectoryRender.BOOT()
        self.magisk_image_container = DirectoryRender.MAGISK("", "")

    def set_item(self, name: str, path: Path) -> Self:
        if name not in self.valid_keys:
            log_status(
                "Error", AttributeError, f"{name} is not in {self.valid_keys}"
            )

        setattr(self, name, path)
        return self


def set_directory_pipeline(parent_directory: Path) -> DirectoryPipeline:
    """Creates a DirectoryTypeDefinition for the specified parent directory."""
    from ..image.image_name import ImageName

    log_status("debug", None, "Creating Directories")
    if not parent_directory.exists() or not parent_directory.is_dir():
        log_status(
            "error",
            SystemExit,
            f"Invalid parent directory: {parent_directory}",
        )

    return (
        DirectoryPipeline()
        .set_item("parent_directory", parent_directory)
        .set_item("_boot_image", ImageName.STOCK.fetch_directory_path())
        .set_item("magisk_image", ImageName.MAGISK.fetch_directory_path())
    )


# Signed off by Brian Sanford on 20260827
