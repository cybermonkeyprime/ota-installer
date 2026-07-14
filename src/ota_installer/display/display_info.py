# display/display_info.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from subprocess import CompletedProcess, run
from typing import Self

from rich.control import Control

from .. import decorator
from ..log_setup import logger
from ..style.style_info import SEPARATOR
from ..versioning.version_info import SoftwareVersion

type DisplayDecorator = Callable[[Callable[[], str]], Callable[[], str]]


class DisplayType(Enum):
    VERBOSE = SoftwareVersion.display()
    CONCISE = SoftwareVersion.formatted()


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()


@dataclass(frozen=True)
class DisplayRenderer:
    """Render a display value with an optional decorator."""

    value: str
    decorator: DisplayDecorator | None = None

    def __call__(self):
        """Return the value processed by the decorator if available."""

        def provider() -> str:
            return self.value

        if self.decorator is None:
            return provider()

        callback = self.decorator(provider)
        return callback()


@dataclass(frozen=True, slots=True)
class DisplayStep:
    """Define one named step in a display pipeline."""

    name: DisplayHeader
    renderer: DisplayRenderer

    @decorator.OutputPrinter(suffix="")
    def run(self) -> str:
        """Render and print this display step."""
        return self.renderer()


HEADER_DISPLAY_STEPS: tuple[DisplayStep, ...] = (
    DisplayStep(
        name=DisplayHeader.TITLE,
        renderer=DisplayRenderer(
            value=f" {SoftwareVersion.TITLE.value}",
            decorator=decorator.StyledFigletPrinter(
                style="title",
                font="slant",
            ),
        ),
    ),
    DisplayStep(
        name=DisplayHeader.MOVE_CURSOR_UP,
        renderer=DisplayRenderer(
            value=str(Control.move(y=-1)),
        ),
    ),
    DisplayStep(
        name=DisplayHeader.SEPARATOR,
        renderer=DisplayRenderer(
            value=f"{SEPARATOR()}> ",
            decorator=decorator.Colorizer(
                style="title",
            ),
        ),
    ),
    DisplayStep(
        name=DisplayHeader.SUBTITLE,
        renderer=DisplayRenderer(
            value=f"{DisplayType.VERBOSE.value}\n",
            decorator=decorator.Colorizer(
                style="version",
            ),
        ),
    ),
)


def process_display_steps(
    steps: tuple[DisplayStep, ...],
) -> None:
    """Process an ordered collection of display steps."""
    for step in steps:
        if not isinstance(step, DisplayStep):
            message = f"Expected DisplayStep, received {type(step).__name__}."
            logger.error(message)
            raise TypeError(message)
        step.run()


@decorator.FooterWrapper(message="")
def process_header_display() -> None:
    """Process all header display steps."""
    process_display_steps(HEADER_DISPLAY_STEPS)


@dataclass(frozen=True, slots=True)
class DisplayHeaderPipeline:
    """Coordinate the header display pipeline."""

    steps: tuple[DisplayStep, ...] = HEADER_DISPLAY_STEPS

    def process_header(self) -> Self:
        """Process the complete display header."""
        process_display_steps(self.steps)
        return self


def clear_screen() -> None:
    """Clears the terminal screen."""
    if not execute_clear_command():
        logger.error("Failed to clear the screen.")


def execute_clear_command() -> CompletedProcess:
    from os import name

    """Executes the command to clear the terminal screen."""
    command = "cls" if name == "nt" else "clear"
    return run(command, check=True, text=True)


def main() -> None:
    """Render the application header."""
    DisplayHeaderPipeline().process_header()


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260628
