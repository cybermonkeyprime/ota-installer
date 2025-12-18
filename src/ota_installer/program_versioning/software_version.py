# src/ota_installer/program_versioning/software_version.py
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum

SoftwareStruct = namedtuple(
    "SoftwareStruct", ["title", "major_number", "minor_number", "patch_number"]
)


class SoftwareVersionConstants(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2025
    MINOR_NUMBER = 12
    PATCH_NUMBER = 16


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    constants: type = field(default_factory=lambda: SoftwareVersionConstants)
    version: list = field(init=False)

    @property
    def data(self) -> list:
        return [enum_member.value for enum_member in SoftwareVersionConstants]

    @property
    def subtitle(self):
        software = SoftwareStruct(*self.data)
        return f"Build: {software.major_number}.{software.minor_number}.{software.patch_number}"
