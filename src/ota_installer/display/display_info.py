# display/display_info.py
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import Enum, StrEnum, auto

from rich.control import Control

from .. import decorator
from ..log_setup import logger
from ..style.style_handler import SEPARATOR
from ..versioning.version_handler import SoftwareVersion

type BoolPredicate = Callable[[], bool]
type DisplayProvidor = Callable[[], str]


class DisplayType(Enum):
    VERBOSE = SoftwareVersion.display()
    CONCISE = SoftwareVersion.formatted()


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @classmethod
    def mapping(cls) -> Mapping[DisplayHeader, DisplayProvidor]:
        """Map enum variants strictly to Callables ensuring a pure pipeline."""
        return {
            cls.TITLE: DisplayContainer(
                f" {SoftwareVersion.TITLE.value}",
                decorator.StyledFigletPrinter(style="title", font="slant"),
            ),
            cls.MOVE_CURSOR_UP: DisplayContainer(
                str(Control.move(y=-1)), None
            ),
            cls.SEPARATOR: DisplayContainer(
                f"{SEPARATOR()}> ",
                decorator.Colorizer(style="title"),
            ),
            cls.SUBTITLE: DisplayContainer(
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
        """Resolve the provider mapping and return the pure string value."""
        provider = self.mapping()[self]
        return provider()

    @classmethod
    @decorator.FooterWrapper(message="")
    def render_all(cls) -> None:
        """Render the display header by invoking the components in sequence."""
        for component in cls.get_rendering_sequence():
            if not cls.execute_component(component):
                logger.error("An error occurred during initialization.")

    @staticmethod
    def execute_component(component: BoolPredicate | None) -> bool:
        """Execute a display component and return success status."""
        return component() if component else False


@dataclass(frozen=True)
class DisplayContainer:
    value: str
    decorator: Callable | None

    def __call__(self):
        def func():
            return self.value

        callback = self.decorator(func) if self.decorator else func
        return callback()


def main() -> None:
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260508
