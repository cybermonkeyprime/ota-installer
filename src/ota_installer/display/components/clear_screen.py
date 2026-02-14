# src/ota_installer/display/managers/clear_screen.py
from os import name
from subprocess import CompletedProcess, run

from ...log_setup import logger


def clear_screen() -> None:
    """Clears the terminal screen."""
    if not execute_clear_command():
        logger.error("Failed to clear the screen.")


def execute_clear_command() -> CompletedProcess:
    """Executes the command to clear the terminal screen."""
    command = "clear" if name != "nt" else "cls"
    result = run(command, check=True)
    if result.returncode != 0:
        raise RuntimeError("Command failed to execute.")
    return result


if __name__ == "__main__":
    clear_screen()

# Signed off by Brian Sanford on 20260203
