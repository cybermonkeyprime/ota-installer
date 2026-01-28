# src/ota_installer/program_versioning/software_version.py
from .builders.software_container_builder import build_software_container


def get_display() -> str:
    """Returns the display string for the global software version."""
    container = build_software_container()
    return f"Build: {container.major_number}.{container.minor_number}.{container.patch_number}"


def get_text_display() -> str:
    """
    Returns a formatted string with the title and display of the software
    version."""
    container = build_software_container()
    return f"{container.title} - {get_display()}"


