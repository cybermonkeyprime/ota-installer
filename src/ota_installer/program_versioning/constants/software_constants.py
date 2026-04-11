# src/ota_installer/program_versioning/constants/software_constants.py
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class SoftwareContainer(object):
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int


class SoftwareType(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 4
    PATCH_NUMBER = 10

    @classmethod
    def build_container(cls) -> SoftwareContainer:
        """Creates a SoftwareContainer instance with versioning information."""
        return SoftwareContainer(
            title=cls.TITLE.value,
            major_number=cls.MAJOR_NUMBER.value,
            minor_number=cls.MINOR_NUMBER.value,
            patch_number=cls.PATCH_NUMBER.value,
        )

    @classmethod
    def render_display(cls) -> str:
        CONTAINER = cls.build_container()
        """Returns the display string for the global software version."""
        return (
            f"Build: {CONTAINER.major_number}."
            f"{CONTAINER.minor_number}.{CONTAINER.patch_number}"
        )

    @classmethod
    def render_text(cls) -> str:
        CONTAINER = cls.build_container()
        """
        Returns a formatted string with the title and display of the software
        version."""
        return f"{CONTAINER.title} - {cls.render_display()}"
