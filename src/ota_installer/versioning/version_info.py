# src/ota_installer/handler/version_handler.py
from dataclasses import dataclass
from enum import Enum


class SoftwareVersion(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 8
    PATCH_NUMBER = 17

    @classmethod
    def to_dict(cls) -> dict:
        return {
            name.lower(): member.value
            for name, member in cls.__members__.items()
        }

    @classmethod
    def software_info(cls):
        return SoftwareInfo(**cls.to_dict())

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

    def display(self) -> str:
        """Returns the display string for the global software version."""
        return (
            f"Build: {self.major_number}."
            f"{self.minor_number}.{self.patch_number}"
        )

    def formatted(self) -> str:
        """
        Returns a formatted string with the title or display of the software
        version."""
        return f"{self.title} - {self.display()}"


# Signed off by Brian Sanford on 20260702
