# src/ota_installer/display/constants/display_header.py
from collections.abc import Callable
from enum import StrEnum, auto

from rich.control import Control

from ... import decorators
from ...decorators import StyledFigletPrinter
from ...decorators.colorizer import Colorizer
from ...log_setup import logger
from ...program_versioning.constants.software_constants import SoftwareType
from ...styles.separator import separator
from ..constants.display_type import DisplayType

type Bool_Predicate = Callable[[], bool]
type Str_Predicate = Callable[[], str]


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @property
    def mapping(self) -> dict["DisplayHeader", Str_Predicate | str]:
        return {
            DisplayHeader.TITLE: _title,
            DisplayHeader.MOVE_CURSOR_UP: str(Control.move(y=-1)),
            DisplayHeader.SEPARATOR: _separator,
            DisplayHeader.SUBTITLE: _subtitle,
        }

    @property
    def build(self) -> str:
        if callable(value := self.mapping[self]):
            return value()

        return value

    @decorators.OutputPrinter(suffix="")
    def render_default(self) -> str:
        """Render the component with default styling."""
        return self.build

    @decorators.OutputPrinter(suffix="")
    @decorators.Colorizer(style="title")
    def render_green(self) -> str:
        """Render the component with green title styling."""
        return self.build

    @classmethod
    def get_rendering_sequence(cls) -> tuple[Bool_Predicate, ...]:
        return (
            cls.TITLE.render_default,
            cls.MOVE_CURSOR_UP.render_default,
            cls.SEPARATOR.render_green,
            cls.SUBTITLE.render_default,
        )

    @classmethod
    @decorators.FooterWrapper(message="")
    def render_all(cls) -> None:
        """Render the display header by invoking the components in sequence."""
        for component in cls.get_rendering_sequence():
            if not cls.execute_component(component):
                logger.error("An error occurred during initialization.")

    @staticmethod
    def execute_component(component: Bool_Predicate | None) -> bool:
        """Execute a display component and return success status."""
        return component() if component else False


@StyledFigletPrinter(style="title", font="slant")
def _title() -> str:
    """
    Generate and return a stylized string representation of the application
        title.
    """
    return f" {SoftwareType.TITLE.value}"


def _separator(indent: int = 9, char: str = "-") -> str:
    """Generates a formatted display separator."""
    formatted_separator = separator()
    return f"{formatted_separator}> "


@Colorizer(style="version")
def _subtitle() -> str:
    """Generate a subtitle displaying the current software version."""
    return DisplayType.VERBOSE.value


def main() -> None:
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
