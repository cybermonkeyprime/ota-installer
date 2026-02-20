# src/tasks/task_operation_constants.py
from enum import Enum, IntEnum, StrEnum, auto


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
    DESCRIPTION = 3
    EXECUTE = 3
    REMINDER = 2
    KEYPRESS = 1


class Messages(Enum):
    """Constants for messages."""

    EXECUTE = "execute the task"


class DefaultIndent(IntEnum):
    """Constants for default indent properties."""

    SPACING = 4
    INTERVAL = 1


# Signed off by Brian Sanford on 20260219
