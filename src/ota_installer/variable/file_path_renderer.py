# src/ota_installer/variable/file_path_renderer.py
from dataclasses import dataclass
from pathlib import Path

from .file_part_renderer import FilePartContainer


@dataclass(frozen=True, slots=True)
class FilePathRenderer:
    """Container for file paths used in the OTA installer."""

    parts: FilePartContainer
    stock: str | None = None
    magisk: str | None = None
    payload: str | None = None

    def __iter__(self):
        return iter(self.__dict__.items())

    def __post_init__(self) -> None:
        self.image_pipeline()

    @property
    def magisk_image_name(self) -> str:
        return "place_holder"

    @property
    def image_data(self) -> "ImageData":
        from ..image.image_containers import ImageData

        return ImageData(self.parts.device, self.parts.build_id)

    @property
    def log_file(self) -> Path:
        """Generate a log file path based on device and version."""
        from tempfile import gettempdir

        return (
            Path(gettempdir())
            / f"ota-installer_{self.parts.device}_{self.parts.build_id}.txt"
        )

    def image_pipeline(self) -> None:
        from ..image.image_name import ImageName

        for key in ImageName.valid_members():
            value = self.image_data(ImageName[key])
            object.__setattr__(self, key.lower(), value)


# Signed off by Brian Sanford on 20260902
