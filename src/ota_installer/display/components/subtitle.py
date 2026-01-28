# src/ota_installer/display/components/subtitle.py

from ...decorators.colorizer import Colorizer
from ...program_versioning.software_version import get_display


@Colorizer(style="version")
def display_subtitle() -> str:
    """Generate a subtitle displaying the current software version.

    Returns:
        str: The string representation of the current software version.
    """
    return get_display()


