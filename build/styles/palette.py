#!/usr/bin/env python3
from dataclasses import dataclass, field

from colorama import init, Fore, Style

init(autoreset=True)


@dataclass
class Colors(object):
    error: str = f"{Fore.RED}{Style.BRIGHT}"
    warning: str = f"{Fore.YELLOW}"
    info: str = f"{Fore.GREEN}{Style.BRIGHT}"
    default: str = Fore.RESET
    debugging: str = Fore.CYAN

    def __post_init__(self):
        self.title: str = self.info
        self.author: str = self.default
        self.version: str = self.warning
        self.separator: str = self.info
        self.variable: str = self.warning

    def __str__(self) -> str:
        return self.debugging


@dataclass
class ColorFormatter(object):
    foreground: str = field(default="")
    style: str = field(default="")

    def __str__(self):
        return f"{self.foreground}{self.style}"


def display_sample_text(style_palette: type) -> bool | None:
    for style_name in style_palette.styles.keys():
        styled_text = style_palette.apply_style("Sample Text", style_name)
        print(styled_text)
    else:
        return True


if __name__ == "__main__":
    style_palette = Colors()
    # display_sample_text(style_palette)
    print(f"{style_palette}Test")
