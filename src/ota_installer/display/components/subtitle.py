# src/ota_installer/display/components/subtitle.py

from ...decorators.colorizer import Colorizer
from ...program_versioning.software_version import SoftwareVersion


@Colorizer(style="version")
def display_subtitle() -> str:
    """Generate a subtitle displaying the current software version.

    Returns:
        str: The string representation of the current software version.
    """
    software_version = SoftwareVersion()
    return software_version.display


# Signed off by Brian Sanford on 20260118
