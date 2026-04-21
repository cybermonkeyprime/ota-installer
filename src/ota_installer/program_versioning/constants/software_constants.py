# src/ota_installer/program_versioning/constants/software_constants.py
from enum import Enum


class SoftwareType(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2026
    MINOR_NUMBER = 4
    PATCH_NUMBER = 21

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
