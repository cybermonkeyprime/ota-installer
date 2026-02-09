# src/ota_installer/tasks/operations/task_operation_details.py
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class TaskOperation(object):
    """Represents a task operation with its details."""

    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None


class TaskOperationDetails(Enum):
    """Enumeration of task operation details."""

    EXTRACT_PAYLOAD_IMAGE = TaskOperation(
        index=1,
        title="Payload Image Extractor",
        description="📦 Extracting payload.bin to access OTA image files.",
    )
    RENAME_PAYLOAD_IMAGE = TaskOperation(
        index=2,
        title="Payload Image Renamer",
        description="📝 Renaming the extracted image file for clarity.",
    )
    EXTRACT_STOCK_BOOT_IMAGE = TaskOperation(
        index=3,
        title="Boot Image Extractor",
        description="🪄  Pulling the boot image from the OTA payload.",
    )
    BACKUP_STOCK_BOOT_IMAGE = TaskOperation(
        index=4,
        title="Backup Stock Boot Image",
        description="📁 Backing up your stock boot image.",
    )
    CHECK_ADB_CONNECTION = TaskOperation(
        index=1,
        title="Check ADB Connection",
        description="🔌 Checking for an ADB-connected device.",
        command_string="adb devices",
    )
    PUSH_STOCK_BOOT_IMAGE = TaskOperation(
        index=2,
        title="Push Stock Boot Image",
        description="📤 Pushing the stock boot image to your device.",
        reminder="Patch boot image in Magisk app",
    )
    FIND_MAGISK_IMAGE = TaskOperation(
        index=3,
        title="Find Magisk Image",
        description="🔍 Searching for the patched Magisk image.",
    )
    PULL_MAGISK_IMAGE = TaskOperation(
        index=4,
        title="Pull Magisk Image",
        description="📥 Pulling the patched Magisk image to your computer.",
    )
    REBOOT_TO_RECOVERY = TaskOperation(
        index=1,
        title="Reboot To Recovery",
        description="♻️ Rebooting the device into recovery mode.",
        command_string="adb reboot recovery",
    )
    APPLY_OTA_UPDATE = TaskOperation(
        index=2,
        title="Apply OTA Image",
        description="🚀 Applying the OTA update via adb sideload.",
        reminder="Restart to verify build, then reboot to Bootloader",
    )
    REBOOT_TO_BOOTLOADER = TaskOperation(
        index=3,
        title="Reboot to Bootloader",
        description="🧰 Rebooting into bootloader (fastboot) mode.",
        command_string="adb reboot bootloader",
    )
    BOOT_TO_MAGISK_IMAGE = TaskOperation(
        index=4,
        title="Boot to Magisk Image",
        description="💾 Flashing the patched Magisk image with fastboot.",
    )


def main():
    pass


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260209
