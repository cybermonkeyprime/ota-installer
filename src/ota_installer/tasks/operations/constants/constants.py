# src/tasks/task_operation_constants.py
from enum import Enum


class TaskOpsConstants(Enum):
    """Constants for task operations."""

    SPACING = 4
    INTERVAL = 1
    TASK_STYLE = "task"


class DescriptionConstants(Enum):
    """Constants for description formatting."""

    INDENT = 3
    STYLE = "warning"


class CommandStringConstants(Enum):
    """Constants for command string formatting."""

    INDENT = 3
    STYLE = "non_error"


class ExecutorConstants(Enum):
    """Constants for task execution."""

    INDENT = 3
    MESSAGE = "execute the task"
    KEYPRESS_INDENT = 1


class ReminderConstants(Enum):
    """Constants for reminder formatting."""

    INDENT = 2
    STYLE = "warning"


class TaskOpsItemTypeConstants(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str


# Signed off by Brian Sanford on 20260202
