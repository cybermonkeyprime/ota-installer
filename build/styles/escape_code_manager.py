from dataclasses import dataclass, field
from typing import Dict
from colorama import Fore, Style

from .palette import ColorFormatter


@dataclass
class EscapeCodeManager(object):
    escape_codes: Dict[str, str] = field(
        default_factory=lambda: {
            "move_cursor_up": "\033[F",
            "title": str(ColorFormatter(Fore.GREEN, Style.BRIGHT)),
        }
    )

    def fetch_escape_code(self, key: str) -> str:
        return self.escape_codes.get(key, "")
