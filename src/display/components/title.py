from dataclasses import dataclass, field

from src.decorators import ColorizedFiglet
import src.display.templates as templates


@dataclass
class Title(templates.DisplayComponent):
    """
    A class representing a title component that can be displayed with special
        formatting.

    Attributes:
        title (str): The title text to be displayed. Defaults to
            "ota-installer".
    """

    title: str = field(default="ota-installer")

    @ColorizedFiglet(style="title", font="slant")
    def return_display(self) -> str:
        """
        Apply the ColorizedFiglet decorator to format the title.

        Returns:
            str: The formatted title string.
        """
        return f" {self.title}"

    def get_display(self) -> str:
        """
        Retrieve the display string of the title, formatted by the
            ColorizedFiglet decorator.

        Returns:
            str: The formatted title string.
        """
        return self.return_display()


@dataclass
class DisplayTitle(Title):
    """
    A class for creating a displayable title string.

    Attributes:
        title (str): The title text to be displayed. Defaults to an empty
            string.
    """

    title: str = field(default_factory=str)

    def __str__(self) -> str:
        """
        Generate a string representation of the DisplayTitle instance, which
            includes the formatted title.

        Returns:
            str: The formatted title string.
        """
        return self.get_display()
