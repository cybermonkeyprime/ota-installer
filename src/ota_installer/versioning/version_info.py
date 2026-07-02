# src/ota_installer/handler/version_handler.py
from dataclasses import dataclass
from enum import Enum


class SoftwareVersion(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 6
    PATCH_NUMBER = 16

    @classmethod
    def display(cls) -> str:
        """Returns the display string for the global software version."""
        return (
            f"Build: {cls.MAJOR_NUMBER.value}."
            f"{cls.MINOR_NUMBER.value}.{cls.PATCH_NUMBER.value}"
        )

    @classmethod
    def formatted(cls) -> str:
        """
        Returns a formatted string with the title or display of the software
        version."""
        return f"{cls.TITLE.value} - {cls.display()}"


@dataclass(frozen=True)
class SoftwareInfo:
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int


# Signed off by Brian Sanford on 20260702
