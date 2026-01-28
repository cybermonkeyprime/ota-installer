# src/ota_installer/display/managers/clear_screen.py
from os import name
from subprocess import CompletedProcess, run


def clear_screen() -> None:
    """Clears the terminal screen."""
    try:
        if execute_clear_command() is None:
            raise RuntimeError("Failed to clear the screen.")
    except RuntimeError as error:
        print(f"An error occurred while trying to clear the screen: {error}")


def execute_clear_command() -> CompletedProcess:
    """Executes the command to clear the terminal screen."""
    command = "clear" if name != "nt" else "cls"
    return run([command])


if __name__ == "__main__":
    clear_screen()

