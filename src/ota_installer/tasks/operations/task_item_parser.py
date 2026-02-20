# src/ota_installer/tasks/operations/task_item_parser.py
from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum

from ... import decorators


class TaskItemConstants(Enum):
    STYLE = "task"


class TaskItemHeaderConstants(Enum):
    INDENT = 1
    STYLE = TaskItemConstants.STYLE.value


class TaskItemAspectConstants(Enum):
    INDENT = 2
    STYLE = TaskItemConstants.STYLE.value


class TaskItemStyles(StrEnum):
    HEADER = TaskItemConstants.STYLE.value
    ASPECT = TaskItemConstants.STYLE.value
    DEFAULT = "tasks"


class TaskItemIndents(IntEnum):
    HEADER = 1
    ASPECT = 2


@dataclass
class TaskItemParser(object):
    """Parser for task items with aspect and header display capabilities."""

    value: str
    constants: type[TaskItemAspectConstants] = TaskItemAspectConstants

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemIndents.ASPECT.value,
        begin="",
        end="",
        style=TaskItemStyles.ASPECT.value,
    )
    def show_aspect(self) -> str:
        """Display the aspect of the task item."""
        return f"{self.value}"

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemIndents.HEADER.value,
        end=":",
        style=TaskItemStyles.HEADER.value,
    )
    def show_header(self) -> str:
        """Display the header of the task item."""
        return f"{self.value}"


# Signed off by Brian Sanford on 20260213
