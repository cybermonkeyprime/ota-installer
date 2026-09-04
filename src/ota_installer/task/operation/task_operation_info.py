# tasks/operations/task_operation_info.py
from dataclasses import dataclass
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


class TaskOpsItemType(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str

    @classmethod
    def get_validated_type(cls, field_name: str) -> type:
        """
        Validates field existence using a whitelist check.
        Raises AttributeError immediately on failure (Fail-Fast).
        """
        key: str = field_name.upper()

        # Explicit membership check: 'Look Before You Leap'
        if not key:
            raise AttributeError(
                f"Invalid field: '{field_name}'. "
                f"Allowed fields are: {', '.join(cls._member_names_)}"
            ) from None

        return cls[key].value


@dataclass
class TaskOperationContainer:
    """Container for task operation details."""

    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None


# Signed off by Brian Sanford on 20260628
