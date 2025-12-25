# src/ota_installer/display/managers/display_screen_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from os import name, system


def default_clear_screen_command() -> int:
    return system("clear" if not name == "nt" else "cls")


@dataclass
class ScreenManager(object):
    clear_command: Callable[[], int] = field(
        default=default_clear_screen_command
    )

    def clear_screen(self) -> None:
        try:
            if self.clear_command() != 0:
                raise RuntimeError("Failed to clear the screen.")
        except RuntimeError as error:
            # Log the error or handle it as needed
            print(
                f"An error occurred while trying to clear the screen: {error}"
            )


if __name__ == "__main__":
    screen_manager = ScreenManager()
    screen_manager.clear_screen()
