# src/ota_installer/tasks/operations/constants/task_ops_item_types.py
from enum import Enum


class TaskOpsItemTypes(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str

    @classmethod
    def validate_and_get_type(cls, field_name: str) -> type:
        """Checks if field exists and returns its expected type."""
        try:
            return cls[field_name.upper()].value
        except KeyError:
            raise AttributeError(
                f"'{field_name}' is not a valid task field."
            ) from None
