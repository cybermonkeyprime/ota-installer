from dataclasses import dataclass, field
from build.styles.palette import Colors


@dataclass
class Colorize:
    """
    A class for styling text with color.

    Attributes:
        style (str): The style to apply to the text.
        value (str): The text content to be styled.
    """
    style: str = field(default="") # Rename to color_style
    value: str = field(default="") # Rename to text_content

    def apply_style(self) -> str:
        """
        Apply the color style to the text content.

        Returns:
            The styled text with color.
        """
        try:
            styled_text = f"{self.style}{self.value}{Colors.reset}"
        except AttributeError:
            styled_text = self.value
        return styled_text

    def __call__(self):
        return self.apply_style()

    def __str__(self):
        return self.apply_style()
