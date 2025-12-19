# src/ota_installer/tasks/constants/migration_task_constants.py
from enum import Enum


class MigrationTaskConstants(Enum):
    CHECK_ADB_CONNECTION = "check_adb_connection"
    PUSH_STOCK_BOOT_IMAGE = "push_stock_boot_image"
    FIND_PATCHED_BOOT_IMAGE = "find_patched_boot_image"
    PULL_PATCHED_BOOT_IMAGE = "pull_patched_boot_image"
