# display/display_info.py
from collections.abc import Callable, Mapping
from enum import Enum, StrEnum, auto

from rich.control import Control

from .. import decorator
from ..log_setup import logger
from ..style.style_handler import separator
from ..versioning.version_handler import SoftwareVersion

type BoolPredicate = Callable[[], bool]
type StrPredicate = Callable[[], str]


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @classmethod
    def mapping(cls) -> Mapping["DisplayHeader", StrPredicate | str]:
        return {
            cls.TITLE: _title,
            cls.MOVE_CURSOR_UP: str(object=Control.move(y=-1)),
            cls.SEPARATOR: _separator,
            cls.SUBTITLE: _subtitle,
        }

    @property
    def build(self) -> str:
        value: StrPredicate | str = self.mapping()[self]
        return value() if callable(value) else value

    @decorator.OutputPrinter(suffix="")
    def render_default(self) -> str:
        """Render the component with default styling."""
        return self.build

    @decorator.OutputPrinter(suffix="")
    @decorator.Colorizer(style="title")
    def render_green(self) -> str:
        """Render the component with green title styling."""
        return self.build

    @classmethod
    def get_rendering_sequence(cls) -> tuple[BoolPredicate, ...]:
        return (
            cls.TITLE.render_default,
            cls.MOVE_CURSOR_UP.render_default,
            cls.SEPARATOR.render_green,
            cls.SUBTITLE.render_default,
        )

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


@decorator.StyledFigletPrinter(style="title", font="slant")
def _title() -> str:
    """
    Generate and return a stylized string representation of the application
        title.
    """
    return f" {SoftwareVersion.TITLE.value}"


def _separator(indent: int = 9, char: str = "-") -> str:
    """Generates a formatted display separator."""
    formatted_separator = separator()
    return f"{formatted_separator}> "


@decorator.Colorizer(style="version")
def _subtitle() -> str:
    """Generate a subtitle displaying the current software version."""
    return f"{DisplayType.VERBOSE.value}\n"


class DisplayType(Enum):
    VERBOSE = SoftwareVersion.display()
    CONCISE = SoftwareVersion.formatted()


def main() -> None:
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260508
