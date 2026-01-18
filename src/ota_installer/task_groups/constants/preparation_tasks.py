# src/ota_installer/task_groups/constants/preparation_tasks.py
from enum import Enum

from ...tasks.constants.task_ids import TaskIDs


class PreparationTasks(Enum):
    """Enumeration of preparation tasks for OTA installation."""

    EXTRACT_PAYLOAD_IMAGE = TaskIDs.EXTRACT_PAYLOAD_IMAGE
    RENAME_PAYLOAD_IMAGE = TaskIDs.RENAME_PAYLOAD_IMAGE
    EXTRACT_STOCK_BOOT_IMAGE = TaskIDs.EXTRACT_STOCK_BOOT_IMAGE
    BACKUP_STOCK_BOOT_IMAGE = TaskIDs.BACKUP_STOCK_BOOT_IMAGE

    @property
    def task_name(self) -> str:
        """Return the lowercase name of the task."""
        return self.value.value.lower()


# Signed off by Brian Sanford on 20260117
