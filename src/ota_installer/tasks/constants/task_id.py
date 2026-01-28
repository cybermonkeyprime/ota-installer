# src/ota_installer/tasks/constants/task_names.py
from enum import StrEnum, auto


class TaskID(StrEnum):
    """Enumeration of task identifiers for OTA installation processes."""

    # preparation
    EXTRACT_PAYLOAD_IMAGE = auto()
    RENAME_PAYLOAD_IMAGE = auto()
    EXTRACT_STOCK_BOOT_IMAGE = auto()
    BACKUP_STOCK_BOOT_IMAGE = auto()
    # migration
    CHECK_ADB_CONNECTION = auto()
    PUSH_STOCK_BOOT_IMAGE = auto()
    FIND_PATCHED_BOOT_IMAGE = auto()
    PULL_PATCHED_BOOT_IMAGE = auto()
    # application
    REBOOT_TO_RECOVERY = auto()
    APPLY_OTA_UPDATE = auto()
    REBOOT_TO_BOOTLOADER = auto()
    BOOT_TO_MAGISK_IMAGE = auto()


