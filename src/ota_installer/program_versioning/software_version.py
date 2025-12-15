# src/ota_installer/program_versioning/software_version.py
from dataclasses import dataclass, field
from enum import Enum


class SoftwareVersionConstants(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2025
    MINOR_NUMBER = 12
    PATCH_NUMBER = 15

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    constants: type = field(default_factory=lambda: SoftwareVersionConstants)
    version: list = field(init=False)

    def __post_init__(self) -> None:
        self.set_version_tag()

    def set_version_tag(self) -> None:
        """Property that generates a version tag string."""
        self.version_tag = f"{self.constants.MAJOR_NUMBER.value}.{self.constants.MINOR_NUMBER.value}.{self.constants.PATCH_NUMBER.value}"

    def display_title(self):
        return (
            f"{self.constants.TITLE}: "
            f"{self.constants.MAJOR_NUMBER.value}."
            f"{self.constants.MINOR_NUMBER.value}."
            f"{self.constants.PATCH_NUMBER.value}"
        )
