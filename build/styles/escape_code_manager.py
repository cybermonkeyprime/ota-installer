from dataclasses import dataclass, field

from colorama import Fore, Style

from build.styles.palette import ColorFormatter


@dataclass
class EscapeCodeManager(object):
    """Manages escape codes for terminal formatting.

    Attributes:
        escape_codes: A dictionary mapping descriptive names to escape codes.
    """

    escape_codes: "dict[str, str]" = field(
        default_factory=lambda: {
            "move_cursor_up": "\033[F",
            "title": str(ColorFormatter(Fore.GREEN, Style.BRIGHT)),
        }
    )

    def fetch_escape_code(self, key: str) -> str:
        """Fetches the escape code associated with the given key.

        Args:
            key: The key for the desired escape code.

        Returns:
            The escape code as a string, or an empty string if not found.
        """
        return self.escape_codes.get(key, "")


if __name__ == "__main__":
    # Example usage of EscapeCodeManager with dependency injection
    escape_code_manager = EscapeCodeManager()
    title_code = escape_code_manager.fetch_escape_code("title")
    print(title_code)
