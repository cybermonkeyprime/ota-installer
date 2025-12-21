# src/ota_installer/task_groups/constants/application_tasks.py
from enum import Enum

from ...tasks.constants.task_ids import TaskIDs


class ApplicationTasks(Enum):
    REBOOT_TO_RECOVERY = TaskIDs.REBOOT_TO_BOOTLOADER
    APPLY_OTA_UPDATE = TaskIDs.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskIDs.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskIDs.BOOT_TO_MAGISK_IMAGE

    @property
    def task_name(self) -> str:
        return self.value.value
