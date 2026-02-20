# src/tasks/task_operation_constants.py
from enum import Enum, IntEnum, StrEnum, auto


class TaskOpsConstants(Enum):
    """Constants for task operations."""

    SPACING = 4
    INTERVAL = 1
    TASK_STYLE = "task"


class Styles(StrEnum):
    """Constants for styles."""

    COMMAND = "non_error"
    NON_ERROR = auto()
    WARNING = auto()
    TASK = auto()
    DESCRIPTION = "warning"


class Indents(IntEnum):
    """Constants for indents."""

    COMMAND = 3
    REMINDER = 2
    EXECUTE = 3
    KEYPRESS = 1
    DESCRIPTION = 3


class Messages(Enum):
    """Constants for messages."""

    EXECUTE = "execute the task"


class Spacings(IntEnum):
    """Constants for spacings."""

    DEFAULT = 4


# Signed off by Brian Sanford on 20260217
