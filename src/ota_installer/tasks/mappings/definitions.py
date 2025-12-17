# src/ota_installer/tasks/mappings/definitions.py
from .constants import TaskGroup, TaskName


class TaskDefinitions:
    def map(self) -> dict[str, list[TaskName]]:
        return {
            TaskGroup.PREPARATION.value: [
                TaskName.EXTRACT_PAYLOAD_IMAGE,
                TaskName.RENAME_PAYLOAD_IMAGE,
                TaskName.EXTRACT_STOCK_BOOT_IMAGE,
                TaskName.BACKUP_STOCK_BOOT_IMAGE,
            ],
            TaskGroup.MIGRATION.value: [
                TaskName.CHECK_ADB_CONNECTION,
                TaskName.PUSH_STOCK_BOOT_IMAGE,
                TaskName.FIND_PATCHED_BOOT_IMAGE,
                TaskName.PULL_PATCHED_BOOT_IMAGE,
                TaskName.REBOOT_TO_RECOVERY,
            ],
            TaskGroup.APPLICATION.value: [
                TaskName.APPLY_OTA_UPDATE,
                TaskName.REBOOT_TO_BOOTLOADER,
                TaskName.BOOT_MAGISK_IMAGE,
            ],
        }
