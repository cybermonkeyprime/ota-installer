# task/operation/task_operation_parser.py
from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum

from ... import decorator


class TaskItemType(Enum):
    STYLE = "task"


class TaskItemAspect(Enum):
    INDENT = 2
    STYLE = TaskItemType.STYLE.value


class TaskItemStyle(StrEnum):
    HEADER = TaskItemType.STYLE.value
    ASPECT = TaskItemType.STYLE.value
    DEFAULT = "tasks"


class TaskItemIndent(IntEnum):
    HEADER = 1
    ASPECT = 2


cip = decorator.ColorizedIndentPrinter(
    indent=TaskItemIndent.ASPECT.value,
    begin="",
    end="",
    style=TaskItemStyle.ASPECT.value,
)


@dataclass
class TaskItemParser:
    """Parser for task items with aspect and header display capabilities."""

    value: str
    constants: type[TaskItemAspect] = TaskItemAspect

    def show_aspect(self) -> str:
        """Display the aspect of the task item."""

        def func():
            return f"{self.value}"

        decorated_func = cip(func)
        return decorated_func()

    @decorator.ColorizedIndentPrinter(
        indent=TaskItemIndent.HEADER.value,
        end="",
        style=TaskItemStyle.HEADER.value,
    )
    def show_header(self) -> str:
        """Display the header of the task item."""
        return f"{self.value}"


