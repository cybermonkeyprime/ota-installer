# src/ota_installer/program_versioning/software_version.py
from enum import Enum

from .builders.software_container_builder import build_software_container

CONTAINER = build_software_container()


def get_display() -> str:
    """Returns the display string for the global software version."""
    return (
        f"Build: {CONTAINER.major_number}."
        f"{CONTAINER.minor_number}.{CONTAINER.patch_number}"
    )


def get_text_display() -> str:
    """
    Returns a formatted string with the title and display of the software
    version."""
    return f"{CONTAINER.title} - {get_display()}"


class DisplayType(Enum):
    VERBOSE = get_display
    CONCISE = get_text_display


