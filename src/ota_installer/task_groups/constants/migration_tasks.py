# src/ota_installer/task_groups/constants/migration_tasks.py
from enum import Enum

from ...tasks.constants.task_ids import TaskIDs


class MigrationTasks(Enum):
    CHECK_ADB_CONNECTION = TaskIDs.CHECK_ADB_CONNECTION
    PUSH_STOCK_BOOT_IMAGE = TaskIDs.PUSH_STOCK_BOOT_IMAGE
    FIND_PATCHED_BOOT_IMAGE = TaskIDs.FIND_PATCHED_BOOT_IMAGE
    PULL_PATCHED_BOOT_IMAGE = TaskIDs.PULL_PATCHED_BOOT_IMAGE

    @property
    def task_name(self) -> str:
        return self.value.value
