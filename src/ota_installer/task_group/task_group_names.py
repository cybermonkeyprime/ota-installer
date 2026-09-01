# src/ota_installer/task_group/task_group_names.py
from enum import StrEnum, auto

from .task_group_pipelines import (
    ApplicationPipeline,
    MigrationPipeline,
    PreparationPipeline,
)
from .task_group_renderer import TaskGroupRenderer

StrTuple = tuple[str, ...]
TaskGroupMap = dict[str, object]


class TaskGroupName(StrEnum):
    """Enumeration for task group names."""

    PREPARATION = auto()
    MIGRATION = auto()
    APPLICATION = auto()

    def _get_value(self, _Class: type) -> object:
        """Retrieve the value from the given object based on the
        task group name.
        """
        return getattr(_Class, self.value)

    @classmethod
    def to_dict(cls) -> dict[str, str]:
        return {member.name: member.value for member in cls}

    @classmethod
    def create_dictionary(cls, obj) -> TaskGroupMap:
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

    @classmethod
    def get_task_group_members(cls) -> StrTuple:
        """Returns the keys of the task groups."""
        return tuple(enum.value for enum in cls)

    @classmethod
    def fetch_mapping(cls) -> dict[str, TaskGroupRenderer]:
        import sys

        module = vars(sys.modules[__name__])

        return {
            member.name: TaskGroupRenderer(
                module[f"{member.value.capitalize()}Pipeline"],
                f"{member.value.capitalize()} Task",
            )
            for member in cls
        }


# Signed off by Brian Sanford on 20260901
