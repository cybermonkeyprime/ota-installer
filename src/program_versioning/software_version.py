# src/programing_version/software_version.py
from dataclasses import dataclass, field
from enum import Enum


class SoftwareVersionConstants(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2025
    MINOR_NUMBER = 12
    PATCH_NUMBER = 7

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    constants: type = field(default_factory=lambda: SoftwareVersionConstants)
    version: list = field(init=False)

    def __post_init__(self) -> None:
        self.set_version()
        self.set_version_tag()

    def set_version(self) -> None:
        self.version = [
            enum_member.value for enum_member in SoftwareVersionConstants
        ]

    def set_version_tag(self) -> None:
        """Property that generates a version tag string."""
        _, major_number, minor_number, patch_number = self.version
        self.version_tag = f"{major_number}.{minor_number}.{patch_number}"

    def display_title(self):
        return f"{self.constants.TITLE}: {self.version_tag}"
