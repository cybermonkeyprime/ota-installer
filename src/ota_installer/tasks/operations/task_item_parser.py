# src/ota_installer/tasks/operations/task_item_parser.py
from dataclasses import dataclass
from enum import Enum

from ... import decorators


class TaskItemConstants(Enum):
    STYLE = "task"


class TaskItemHeaderConstants(Enum):
    INDENT = 1
    STYLE = TaskItemConstants.STYLE.value


class TaskItemAspectConstants(Enum):
    INDENT = 2
    STYLE = TaskItemConstants.STYLE.value


@dataclass
class TaskItemParser(object):
    """Parser for task items with aspect and header display capabilities."""

    value: str
    constants: type[TaskItemAspectConstants] = TaskItemAspectConstants

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemAspectConstants.INDENT.value,
        begin="",
        end="",
        style=TaskItemAspectConstants.STYLE.value,
    )
    def show_aspect(self) -> str:
        """Display the aspect of the task item."""
        return f"{self.value}"

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemHeaderConstants.INDENT.value,
        end=":",
        style=TaskItemHeaderConstants.STYLE.value,
    )
    def show_header(self) -> str:
        """Display the header of the task item."""
        return f"{self.value}"


