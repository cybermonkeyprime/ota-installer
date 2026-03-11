# src/ota_installer/tasks/constants/task_names.py
from collections.abc import Callable
from enum import StrEnum, auto

from ..plugin_registry import TASK_PLUGINS


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

    @property
    def execute(self) -> Callable:
        """
        The Dispatcher: Fetches the registered plugin function.
        Fails loudly if the task exists in TaskID but wasn't loaded.
        """
        if self.value not in TASK_PLUGINS:
            raise NotImplementedError(
                f"LOUD FAIL: TaskID.{self.name} ('{self.value}') has no "
                f"registered plugin. Check plugin_loader.py imports!"
            )

        return TASK_PLUGINS[self.value]


# Signed off by Brian Sanford on 20260303
