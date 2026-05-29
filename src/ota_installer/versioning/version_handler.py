# src/ota_installer/handler/version_handler.py
from dataclasses import dataclass
from enum import Enum


class SoftwareVersion(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 5
    PATCH_NUMBER = 22

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


def create_software_info() -> SoftwareInfo:
    """Creates a SoftwareContainer instance with versioning information."""
    return SoftwareInfo(
        title=SoftwareVersion.TITLE.value,
        major_number=SoftwareVersion.MAJOR_NUMBER.value,
        minor_number=SoftwareVersion.MINOR_NUMBER.value,
        patch_number=SoftwareVersion.PATCH_NUMBER.value,
    )


# Signed off by Brian Sanford on 20260523
