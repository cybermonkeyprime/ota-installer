#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import Dict

from colorama import Fore, Style


@dataclass
class Colors(object):
    title: str = f"{Fore.GREEN}{Style.BRIGHT}"
    author: str = f"{Fore.WHITE}{Style.DIM}"
    version: str = f"{Fore.YELLOW}"
    separator: str = f"{Fore.GREEN}{Style.BRIGHT}"
    task: str = f"{Fore.GREEN}{Style.BRIGHT}"
    variable: str = f"{Fore.YELLOW}"
    reset: str = f"{Style.RESET_ALL}"
    error: str = f"{Fore.RED}{Style.BRIGHT}"
    warning: str = f"{Fore.YELLOW}"
    non_error: str = f"{Fore.WHITE}"


@dataclass
class ColorFormatter(object):
    foreground: str = field(default="")
    style: str = field(default="")

    def __str__(self):
        return f"{self.foreground}{self.style}"


class StylePalette(ColorFormatter):
    styles: Dict[str, ColorFormatter] = field(
        default_factory=lambda: {
            "title": ColorFormatter(Fore.GREEN, Style.BRIGHT),
            "author": ColorFormatter(Fore.WHITE, Style.DIM),
            "version": ColorFormatter(Fore.YELLOW, ""),
            "separator": ColorFormatter(Fore.GREEN, Style.BRIGHT),
            "task": ColorFormatter(Fore.GREEN, Style.BRIGHT),
            "variable": ColorFormatter(Fore.YELLOW, ""),
            "reset": ColorFormatter("", Style.RESET_ALL),
            "error": ColorFormatter(Fore.RED, Style.BRIGHT),
            "warning": ColorFormatter(Fore.YELLOW, ""),
            "non_error": ColorFormatter(Fore.WHITE, ""),
        }
    )

    def get_style_code(self, style_name: str) -> ColorFormatter | str:
        return self.styles.get(style_name, "Fore.BLUE")

    def apply_style(self, text: str, style_name: str) -> str:
        try:
            style_code = self.get_style_code(style_name)
            return f"{style_code}{text}{self.styles['reset']}"
        except KeyError as e:
            return f"{self.styles['error']}Error: Style '{style_name}' not found.{self.styles['reset']}"

    def __call__(self, style_name: str):
        return self.get_style_code(style_name)


def display_sample_text(style_palette: StylePalette) -> None:
    for style_name in style_palette.styles.keys():
        styled_text = style_palette.apply_style("Sample Text", style_name)
        print(styled_text)


if __name__ == "__main__":
    style_palette = StylePalette()
    display_sample_text(style_palette)
