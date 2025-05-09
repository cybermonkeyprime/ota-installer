from dataclasses import dataclass, field
from typing import Optional

from colorama import Fore, Style, init

init(autoreset=True)


@dataclass
class Colors(object):  # Rename StylePalette
    """Represents a palette of styles for console output."""

    error: str = f"{Fore.RED}{Style.BRIGHT}"
    warning: str = f"{Fore.YELLOW}"
    info: str = f"{Fore.GREEN}{Style.BRIGHT}"
    default: str = Fore.RESET
    debugging: str = Fore.CYAN
    title: str = field(default_factory=lambda: f"{Fore.GREEN}{Style.BRIGHT}")
    author: str = default
    version: str = warning
    separator: str = info
    variable: str = warning

    def apply_style(self, text: str, style_name: str) -> str:
        """Applies the given style to the text."""
        style = getattr(self, style_name, self.default)
        return f"{style}{text}{Style.RESET_ALL}"

    def __str__(self) -> str:
        return self.debugging


@dataclass
class ColorFormatter(object):
    """Formats text with foreground color and style."""

    foreground: str = field(default="")
    style: str = field(default="")

    def __str__(self):
        return f"{self.foreground}{self.style}"

    def format_text(self, text: str) -> str:
        """Formats the given text with the formatter's style."""
        return f"{self.foreground}{self.style}{text}{Style.RESET_ALL}"


def display_sample_text(style_palette: Colors) -> Optional[bool]:
    """Displays sample text with all styles from the given palette."""
    try:
        for style_name in style_palette.__annotations__.keys():
            styled_text = style_palette.apply_style("Sample Text", style_name)
            print(styled_text)
        return True
    except ColorError as err:
        print(f"{style_palette.error}Error applying styles: {err}")
        return None

class ColorError(Exception):
    pass

if __name__ == "__main__":
    style_palette = Colors()
    # display_sample_text(style_palette)
    print(f"{style_palette}Test")
