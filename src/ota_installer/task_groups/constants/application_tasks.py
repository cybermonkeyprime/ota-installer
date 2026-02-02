# src/ota_installer/task_groups/constants/application_tasks.py
from enum import Enum

from ...tasks.constants.task_id import TaskID


class ApplicationTasks(Enum):
    """Enumeration of application tasks for OTA installation."""

    REBOOT_TO_RECOVERY = TaskID.REBOOT_TO_RECOVERY
    APPLY_OTA_UPDATE = TaskID.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskID.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskID.BOOT_TO_MAGISK_IMAGE

    @property
    def task_name(self) -> str:
        """Returns the name of the task associated with the enum value."""
        return self.value.value


# Signed off by Brian Sanford on 20260202
