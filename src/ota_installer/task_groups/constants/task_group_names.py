# task_groups/constants/task_group_names.py
from enum import StrEnum, auto


class TaskGroupNames(StrEnum):
    """Enumeration for task group names."""

    PREPARATION = auto()
    MIGRATION = auto()
    APPLICATION = auto()

    def _get_value(self, obj: type) -> object:
        """Retrieve the value from the given object based on the
        task group name.
        """
        return getattr(obj, self.value)

    @classmethod
    def create_dictionary(cls, obj) -> dict:
        """create the dictionary with enum member names and their
        corresponding values.
        """
        return {
            enum_member: enum_member._get_value(obj) for enum_member in cls
        }

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()

    @classmethod
    def validation(cls, value: str) -> bool:
        """Validate the provided task group name."""
        return value.upper() in cls.__members__


# Signed off by Brian Sanford on 20260303
