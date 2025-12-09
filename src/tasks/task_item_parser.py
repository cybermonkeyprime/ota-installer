# src/tasks/task_item_parser.py
from dataclasses import dataclass
from enum import Enum

from src import decorators


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
    value: str

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemAspectConstants.INDENT.value,
        begin="",
        end="",
        style=TaskItemAspectConstants.STYLE.value,
    )
    def show_aspect(self) -> str:
        return f"{self.value}"

    @decorators.ColorizedIndentPrinter(
        indent=TaskItemHeaderConstants.INDENT.value,
        end=":",
        style=TaskItemHeaderConstants.STYLE.value,
    )
    def show_header(self) -> str:
        return f"{self.value}"
