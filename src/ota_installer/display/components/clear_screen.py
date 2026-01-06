# src/ota_installer/display/managers/clear_screen.py
from os import name, system


def default_clear_screen_command() -> int:
    return system("clear" if not name == "nt" else "cls")


def clear_screen() -> None:
    try:
        if default_clear_screen_command() != 0:
            raise RuntimeError("Failed to clear the screen.")
    except RuntimeError as error:
        # Log the error or handle it as needed
        print(f"An error occurred while trying to clear the screen: {error}")


if __name__ == "__main__":
    clear_screen()
