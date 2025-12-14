# src/ota_installer/display/components/title.py
from dataclasses import dataclass, field

import src.ota_installer.display.templates as templates
from src.ota_installer.decorators import StyledFigletPrinter


@dataclass
class Title(templates.DisplayComponent):
    """
    A class representing a title component that can be displayed with special
        formatting.
    """

    title: str = field(default="ota-installer")

    @StyledFigletPrinter(style="title", font="slant")
    def return_display(self) -> str:
        """
        Apply the ColorizedFiglet decorator to format the title.
        """
        return f" {self.title}"

    def get_display(self) -> str:
        """
        Retrieve the display string of the title, formatted by the
            ColorizedFiglet decorator.
        """
        return self.return_display()


@dataclass
class DisplayTitle(Title):
    """
    A class for creating a displayable title string.
    """

    title: str = field(default_factory=str)

    def __str__(self) -> str:
        """
        Generate a string representation of the DisplayTitle instance, which
            includes the formatted title.
        """
        return self.get_display()
