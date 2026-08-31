# src/ota_installer/image/boot/boot_image_container.py
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from ..image_name import ImageName


@dataclass(frozen=True, slots=True)
class BootImageContainer:
    """Container for boot image paths."""

    stock: Path

    magisk: Path

    @classmethod
    def create(cls) -> Self:
        return cls(**ImageName.boot_directories())


# Signed off by Brian Sanford on 20260831
