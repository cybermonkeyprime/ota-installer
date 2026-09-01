# src/ota_installer/task/task_group_pipelines.py
from enum import Enum

from ..task.task_info import TaskID

StrTuple = tuple[str, ...]


class BehaviorBase(Enum):
    @property
    def task_name(self) -> str:
        """Return the lowercase name of the task."""
        return self.value.value

    @classmethod
    def get_member_names(cls) -> StrTuple:
        """Extracts task names from an enumeration."""
        return tuple(enum_member.value.value for enum_member in cls)


class ApplicationPipeline(BehaviorBase):
    """Enumeration of application tasks for OTA installation."""

    REBOOT_TO_RECOVERY = TaskID.REBOOT_TO_RECOVERY
    APPLY_OTA_UPDATE = TaskID.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskID.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskID.BOOT_TO_MAGISK_IMAGE


class MigrationPipeline(BehaviorBase):
    """Enumeration of migration tasks with associated task IDs."""

    CHECK_ADB_CONNECTION = TaskID.CHECK_ADB_CONNECTION
    PUSH_STOCK_IMAGE = TaskID.PUSH_STOCK_IMAGE
    FIND_MAGISK_IMAGE = TaskID.FIND_MAGISK_IMAGE
    PULL_MAGISK_IMAGE = TaskID.PULL_MAGISK_IMAGE


class PreparationPipeline(BehaviorBase):
    """Enumeration of preparation tasks for OTA installation."""

    EXTRACT_PAYLOAD_IMAGE = TaskID.EXTRACT_PAYLOAD_IMAGE
    RENAME_PAYLOAD_IMAGE = TaskID.RENAME_PAYLOAD_IMAGE
    EXTRACT_STOCK_BOOT_IMAGE = TaskID.EXTRACT_STOCK_BOOT_IMAGE
    BACKUP_STOCK_BOOT_IMAGE = TaskID.BACKUP_STOCK_BOOT_IMAGE


# Signed off by Brian Sanford on 20260831
