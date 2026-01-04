# src/ota_installer/program_versioning/software_version.py
from dataclasses import dataclass

from .builders.software_container_builder import build_software_container


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    sc = build_software_container()

    @property
    def display(self):
        return f"Build: {self.sc.major_number}.{self.sc.minor_number}.{self.sc.patch_number}"

    def get_display(self):
        sc = build_software_container()
        return f"Build: {self.sc.major_number}.{self.sc.minor_number}.{self.sc.patch_number}"


SC = build_software_container()


def get_display():
    return f"Build: {SC.major_number}.{SC.minor_number}.{SC.patch_number}"


def get_text_display():
    return f"{SC.title} - {get_display()}"
