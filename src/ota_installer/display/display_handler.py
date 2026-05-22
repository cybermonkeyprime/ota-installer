from collections.abc import Callable
from dataclasses import dataclass
from functools import singledispatchmethod
from os import name
from subprocess import CompletedProcess, run

from ..log_setup import logger


@dataclass(frozen=True, slots=True)
class DisplayObjectProcessor(object):
    """
    Processor class for creating display objects based on the provided
        callable and argument.
    """

    function: Callable

    @singledispatchmethod
    def process_object(self, argument: str | object | None) -> str:
        """Process the provided argument using a callable."""
        raise ValueError(f"Unsupported type: {type(argument).__name__}")

    @process_object.register
    def _(self) -> str:
        """Process the argument when it is None."""
        return self.function()

    @process_object.register
    def _(self, argument: str) -> str:
        """Process the argument when it is a string."""
        return self.function(argument)


def clear_screen() -> None:
    """Clears the terminal screen."""
    if not execute_clear_command():
        logger.error("Failed to clear the screen.")


def execute_clear_command() -> CompletedProcess:
    """Executes the command to clear the terminal screen."""
    command = "cls" if name == "nt" else "clear"
    result = run(command, check=True)
    if result.returncode != 0:
        raise RuntimeError("Command failed to execute.")
    return result


if __name__ == "__main__":
    clear_screen()
