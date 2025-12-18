# src/ota_installer/display/components/subtitle.py

from dataclasses import dataclass

from ...decorators.colorizer import Colorizer
from ...program_versioning.software_version import SoftwareVersion
from ..templates import DisplayComponent


@dataclass
class Subtitle(DisplayComponent):
    """
    Subtitle class that inherits from DisplayComponent and is responsible for
    creating a subtitle display element with version details.
    """

    @Colorizer(style="version")
    def get_display(self) -> str:
        """
        Apply colorization to the subtitle text and return the display string
        with the software version tag.
        """

        return SoftwareVersion().sub_title


class DisplaySubtitle(Subtitle):
    """
    DisplaySubtitle class that inherits from Subtitle and is responsible for
    representing the subtitle as a string.
    """

    def __str__(self) -> str:
        """
        String representation of the DisplaySubtitle instance.
        """

        return self.get_display()
