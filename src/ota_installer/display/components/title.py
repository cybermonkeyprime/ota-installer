# src/ota_installer/display/components/title.py

from ...decorators import StyledFigletPrinter
from ...program_versioning.constants.software_constants import (
    SoftwareConstants,
)


@StyledFigletPrinter(style="title", font="slant")
def display_title() -> str:
    """
    Generate a string representation of the display_title instance, which
        includes the formatted title.
    """
    title = SoftwareConstants.TITLE.value
    return f" {title}"
