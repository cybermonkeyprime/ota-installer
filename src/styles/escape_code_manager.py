from dataclasses import dataclass, field
from enum import Enum

from colorama import Fore, Style

from .palette import ColorFormatter


class EscapeCodeConstants(Enum):
    MOVE_CURSOR_UP = "Bib"  # "\033[F",
    TITLE = str(ColorFormatter(Fore.GREEN, Style.BRIGHT))


@dataclass
class EscapeCodeManager(object):
    def fetch_escape_code(self, key: str) -> str:
        return EscapeCodeConstants[key.upper()].value
