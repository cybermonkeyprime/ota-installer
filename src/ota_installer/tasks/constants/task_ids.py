# src/ota_installer/tasks/constants/task_names.py
from enum import Enum


class TaskIDs(Enum):
    # preparation
    EXTRACT_PAYLOAD_IMAGE = "extract_payload_image"
    RENAME_PAYLOAD_IMAGE = "rename_payload_image"
    EXTRACT_STOCK_BOOT_IMAGE = "extract_stock_boot_image"
    BACKUP_STOCK_BOOT_IMAGE = "backup_stock_boot_image"
    # migration
    CHECK_ADB_CONNECTION = "check_adb_connection"
    PUSH_STOCK_BOOT_IMAGE = "push_stock_boot_image"
    FIND_PATCHED_BOOT_IMAGE = "find_patched_boot_image"
    PULL_PATCHED_BOOT_IMAGE = "pull_patched_boot_image"
    # application
    REBOOT_TO_RECOVERY = "reboot_to_recovery"
    APPLY_OTA_UPDATE = "apply_ota_update"
    REBOOT_TO_BOOTLOADER = "reboot_to_bootloader"
    BOOT_TO_MAGISK_IMAGE = "boot_to_magisk_image"

    @property
    def task_name(self) -> str:
        return self.value.lower()
