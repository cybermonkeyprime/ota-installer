# src/ota_installer/task_groups/constants/application_tasks.py
from enum import Enum

from ...log_setup import logger
from ...tasks.constants.task_id import TaskID


class ApplicationTask(Enum):
    """Enumeration of application tasks for OTA installation."""

    REBOOT_TO_RECOVERY = TaskID.REBOOT_TO_RECOVERY
    APPLY_OTA_UPDATE = TaskID.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskID.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskID.BOOT_TO_MAGISK_IMAGE

    @property
    def task_name(self) -> str:
        """Returns the name of the task associated with the enum value."""
        return self.value.value

    @classmethod
    def get_member_names(cls) -> tuple[str, ...]:
        """Extracts task names from an enumeration."""
        result = tuple(enum_member.value.value for enum_member in cls)
        logger.debug(f"enum_task_names(): {result=}")
        return result


# Signed off by Brian Sanford on 20260318
