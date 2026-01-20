# src/ota_installer/task_groups/constants/migration_task.py
from enum import Enum

from ...tasks.constants.task_id import TaskID


class MigrationTask(Enum):
    """Enumeration of migration tasks with associated task IDs."""

    CHECK_ADB_CONNECTION = TaskID.CHECK_ADB_CONNECTION
    PUSH_STOCK_BOOT_IMAGE = TaskID.PUSH_STOCK_BOOT_IMAGE
    FIND_PATCHED_BOOT_IMAGE = TaskID.FIND_PATCHED_BOOT_IMAGE
    PULL_PATCHED_BOOT_IMAGE = TaskID.PULL_PATCHED_BOOT_IMAGE

    @property
    def task_name(self) -> str:
        """Returns the name of the task."""
        return self.value.value


# Signed off by Brian Sanford on 20260120
