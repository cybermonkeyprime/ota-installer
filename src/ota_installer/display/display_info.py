# display/display_info.py
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from subprocess import CompletedProcess, run

from rich.control import Control

from .. import decorator
from ..log_setup import logger
from ..versioning.version_info import SoftwareVersion

type BoolPredicate = Callable[[], bool]
type DisplayProvidor = Callable[[], str]


class DisplayType(Enum):
    VERBOSE = SoftwareVersion.display()
    CONCISE = SoftwareVersion.formatted()


@dataclass(frozen=True)
class DisplayRenderer:
    value: str
    decorator: Callable | None

    def __call__(self):
        """Return the value processed by the decorator if available."""

        def func():
            return self.value

        callback = self.decorator(func) if self.decorator else func

        return callback()


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @classmethod
    def mapping(cls) -> Mapping[DisplayHeader, DisplayProvidor]:
        from ..style.style_info import SEPARATOR

        """Map enum variants strictly to Callables ensuring a pure pipeline."""
        return {
            cls.TITLE: DisplayRenderer(
                f" {SoftwareVersion.TITLE.value}",
                decorator.StyledFigletPrinter(style="title", font="slant"),
            ),
            cls.MOVE_CURSOR_UP: DisplayRenderer(str(Control.move(y=-1)), None),
            cls.SEPARATOR: DisplayRenderer(
                f"{SEPARATOR()}> ",
                decorator.Colorizer(style="title"),
            ),
            cls.SUBTITLE: DisplayRenderer(
                f"{DisplayType.VERBOSE.value}\n",
                decorator.Colorizer(style="version"),
            ),
        }

    @classmethod
    def get_rendering_sequence(cls) -> tuple[BoolPredicate, ...]:
        return (
            cls.TITLE.render,
            cls.MOVE_CURSOR_UP.render,
            cls.SEPARATOR.render,
            cls.SUBTITLE.render,
        )

    @decorator.OutputPrinter(suffix="")
    def render(self):
        """Render the display component as a string."""
        provider = self.mapping()[self]
        return provider()

    @classmethod
    @decorator.FooterWrapper(message="")
    def render_all(cls) -> None:
        """Render all display headers in sequence."""
        for component in cls.get_rendering_sequence():
            if not cls.execute_component(component):
                logger.error("An error occurred during initialization.")

    @staticmethod
    def execute_component(component: BoolPredicate | None) -> bool:
        """Execute a display component and return success status."""
        return component() if component else False


@dataclass(frozen=True, slots=True)
class DisplayObjectProcessor:
    """
    Processor class for creating display objects based on the provided
        callable and argument.
    """

    from functools import singledispatchmethod

    func: Callable

    @singledispatchmethod
    def process_object(self, argument: str | object | None) -> str:
        """Process the provided argument using a callable."""
        raise ValueError(f"Unsupported type: {type(argument).__name__}")

    @process_object.register
    def _(self) -> str:
        """Process the argument when it is None."""
        return self.func()

    @process_object.register
    def _(self, argument: str) -> str:
        """Process the argument when it is a string."""
        return self.func(argument)


def clear_screen() -> None:
    """Clears the terminal screen."""
    if not execute_clear_command():
        logger.error("Failed to clear the screen.")


def execute_clear_command() -> CompletedProcess:
    from os import name

    """Executes the command to clear the terminal screen."""
    command = "cls" if name == "nt" else "clear"
    result = run(command, check=True)
    if result.returncode != 0:
        raise RuntimeError("Command failed to execute.")
    return result


def main() -> None:
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260612
