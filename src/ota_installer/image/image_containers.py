# src/ota_installer/image/image_containers.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ImagePaths:
    """Represents file and directory paths for a file image."""

    file_path: Path
    directory_path: Path


@dataclass(frozen=True, slots=True)
class ImageData:
    """Contains information about the file image data."""

    device: str
    build_id: str

    def __call__(self, image: ImageName | str) -> Path:
        from .image_name import ImageName

        if isinstance(image, ImageName):
            return image.path(self.device, self.build_id)

        return ImageName[image.upper()].path(
            self.device,
            self.build_id,
        )


@dataclass(frozen=True, slots=True)
class ImageRenderer:
    directory: Path
    title: str
    extension: str

    def path(self, device: str, build_id: str) -> Path:
        return (
            self.directory
            / f"{device}-{self.title}-{build_id}.{self.extension}"
        )


# Signed off by Brian Sanford on 20260831
