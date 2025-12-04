# src/tasks/task_operation_constants.py
from enum import Enum


class TaskOpsConstants(Enum):
    SPACING = 4
    INTERVAL = 1
    TASK_STYLE = "task"


class DescriptionConstants(Enum):
    INDENT = 3
    STYLE = "warning"


class CommandStringConstants(Enum):
    INDENT = 3
    STYLE = "non_error"


class ExecutorConstants(Enum):
    INDENT = 2
    MESSAGE = "execute the task"
    KEYPRESS_INDENT = 1


class ReminderConstants(Enum):
    INDENT = 2
    STYLE = TaskOpsConstants.TASK_STYLE.value


class TaskOpsItemTypeConstants(Enum):
    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str
