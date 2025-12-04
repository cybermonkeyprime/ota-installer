from dataclasses import dataclass, field

from src.display.templates.display_template import DisplayComponent
import styles


@dataclass
class Separator(DisplayComponent):
    """
    A class representing a separator component in a display.

    Attributes:
        indent (int): The indentation level for the separator.
        char (str): The character used to create the separator line.

    Methods:
        return_display: Creates a styles.Separator object with the specified
            indent and char.
        get_display: Returns the styles.Separator object.
    """

    indent: int = field(default=0)
    char: str = field(default="")

    def return_display(self) -> styles.Separator:
        """
        Creates and returns a styles.Separator object with the current indent
            and char.

        Returns:
            styles.Separator: The created styles.Separator object.
        """
        return styles.Separator(self.indent, self.char)

    def get_display(self) -> object:
        """
        Returns the display representation of the separator.

        Returns:
            object: The display representation of the separator.
        """
        return self.return_display()


@dataclass
class DisplaySeparator(object):
    """
    A class for creating a display separator with a specified indentation
        and character.

    Attributes:
        indent (int): The indentation level for the separator.
        char (str): The character used to create the separator line.

    Methods:
        __str__: Returns a string representation of the display separator.
    """

    indent: int = field(default=9)
    char: str = field(default="-")

    def __str__(self) -> str:
        """
        Returns a string representation of the display separator.

        Returns:
            str: The string representation of the display separator.
        """
        component = Separator(self.indent, self.char[0])
        return f"{component.get_display()}> "
