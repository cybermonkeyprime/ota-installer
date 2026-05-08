# version_handler.py
from dataclasses import dataclass
from enum import Enum


class SoftwareType(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 5
    PATCH_NUMBER = 8

    @classmethod
    def render_display(cls) -> str:
        """Returns the display string for the global software version."""
        return (
            f"Build: {cls.MAJOR_NUMBER.value}."
            f"{cls.MINOR_NUMBER.value}.{cls.PATCH_NUMBER.value}"
        )

    @classmethod
    def render_text(cls) -> str:
        """
        Returns a formatted string with the title or display of the software
        version."""
        return f"{cls.TITLE.value} - {cls.render_display()}"


@dataclass(frozen=True, slots=True)
class SoftwareContainer(object):
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int


def build_software_container() -> SoftwareContainer:
    """Creates a SoftwareContainer instance with versioning information."""
    return SoftwareContainer(
        title=SoftwareType.TITLE.value,
        major_number=SoftwareType.MAJOR_NUMBER.value,
        minor_number=SoftwareType.MINOR_NUMBER.value,
        patch_number=SoftwareType.PATCH_NUMBER.value,
    )


# Signed off by Brian Sanford on 20260508
