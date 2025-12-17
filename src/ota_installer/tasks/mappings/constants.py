# src/ota_installer/tasks/mappings/constants.py
from collections import namedtuple
from enum import Enum

TaskGroupData = namedtuple("TaskGroupData", ["group_name", "group_enum"])


class TaskGroup(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"


class PreparationTasks(Enum):
    EXTRACT_PAYLOAD_IMAGE = "extract_payload_image"
    RENAME_PAYLOAD_IMAGE = "rename_payload_image"
    EXTRACT_STOCK_BOOT_IMAGE = "extract_stock_boot_image"
    BACKUP_STOCK_BOOT_IMAGE = "backup_stock_boot_image"


class MigrationTasks(Enum):
    CHECK_ADB_CONNECTION = "check_adb_connection"
    PUSH_STOCK_BOOT_IMAGE = "push_stock_boot_image"
    FIND_PATCHED_BOOT_IMAGE = "find_patched_boot_image"
    PULL_PATCHED_BOOT_IMAGE = "pull_patched_boot_image"


class ApplicationTasks(Enum):
    REBOOT_TO_RECOVERY = "reboot_to_recovery"
    ADB_SIDELOAD = "adb_sideload"
    REBOOT_TO_BOOTLOADER = "reboot_to_bootloader"
    BOOT_MAGISK_IMAGE = "boot_magisk_image"


class TaskGroupInfo(Enum):
    PREPARATION = TaskGroupData("preparation", PreparationTasks)
    MIGRATION = TaskGroupData("migration", PreparationTasks)
    APPLICATION = TaskGroupData("application", ApplicationTasks)

    @property
    def group_name(self) -> str:
        return self.value.group_name

    @property
    def group_enum(self) -> str:
        return self.value.group_enum


class TaskName(Enum):
    EXTRACT_PAYLOAD_IMAGE = PreparationTasks.EXTRACT_PAYLOAD_IMAGE.value
    RENAME_PAYLOAD_IMAGE = PreparationTasks.RENAME_PAYLOAD_IMAGE.value
    EXTRACT_STOCK_BOOT_IMAGE = PreparationTasks.EXTRACT_STOCK_BOOT_IMAGE.value
    BACKUP_STOCK_BOOT_IMAGE = PreparationTasks.BACKUP_STOCK_BOOT_IMAGE.value
    CHECK_ADB_CONNECTION = MigrationTasks.CHECK_ADB_CONNECTION.value
    PUSH_STOCK_BOOT_IMAGE = MigrationTasks.PUSH_STOCK_BOOT_IMAGE.value
    FIND_PATCHED_BOOT_IMAGE = MigrationTasks.FIND_PATCHED_BOOT_IMAGE.value
    PULL_PATCHED_BOOT_IMAGE = MigrationTasks.PULL_PATCHED_BOOT_IMAGE.value
    REBOOT_TO_RECOVERY = ApplicationTasks.REBOOT_TO_RECOVERY.value
    ADB_SIDELOAD = ApplicationTasks.ADB_SIDELOAD.value
    REBOOT_TO_BOOTLOADER = ApplicationTasks.REBOOT_TO_BOOTLOADER.value
    BOOT_MAGISK_IMAGE = ApplicationTasks.BOOT_MAGISK_IMAGE.value

    @property
    def lower_case(self) -> str:
        return self.value.lower()
