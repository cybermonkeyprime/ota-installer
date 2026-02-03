# src/ota_installer/tasks/operations/task_operation_details.py
from enum import Enum

from ..containers.task_operation_container import TaskOperationContainer


class TaskOperationDetails(Enum):
    EXTRACT_PAYLOAD_IMAGE = TaskOperationContainer(
        index=1,
        title="Payload Image Extractor",
        description="📦 Extracting payload.bin to access OTA image files.",
    )
    RENAME_PAYLOAD_IMAGE = TaskOperationContainer(
        index=2,
        title="Payload Image Renamer",
        description="📝 Renaming the extracted image file for clarity.",
    )
    EXTRACT_STOCK_BOOT_IMAGE = TaskOperationContainer(
        index=3,
        title="Boot Image Extractor",
        description="🪄  Pulling the boot image from the OTA payload.",
    )
    BACKUP_STOCK_BOOT_IMAGE = TaskOperationContainer(
        index=4,
        title="Backup Stock Boot Image",
        description="📁 Backing up your stock boot image.",
    )
    CHECK_ADB_CONNECTION = TaskOperationContainer(
        index=1,
        title="Check ADB Connection",
        description="🔌 Checking for an ADB-connected device.",
        command_string="adb devices",
    )
    PUSH_STOCK_BOOT_IMAGE = TaskOperationContainer(
        index=2,
        title="Push Stock Boot Image",
        description="📤 Pushing the stock boot image to your device.",
        reminder="Patch boot image in Magisk app",
    )
    FIND_MAGISK_IMAGE = TaskOperationContainer(
        index=3,
        title="Find Magisk Image",
        description="🔍 Searching for the patched Magisk image.",
    )
    REBOOT_TO_RECOVERY = TaskOperationContainer(
        index=1,
        title="Reboot To Recovery",
        description="♻️ Rebooting the device into recovery mode.",
        command_string="adb reboot recovery",
    )

    APPLY_OTA_UPDATE = TaskOperationContainer(
        index=2,
        title="Apply OTA Image",
        description="🚀 Applying the OTA update via adb sideload.",
        reminder="Restart to verify build, then reboot to Bootloader",
    )
    REBOOT_TO_BOOTLOADER = TaskOperationContainer(
        index=3,
        title="Reboot to Bootloader",
        description="🧰 Rebooting into bootloader (fastboot) mode.",
        command_string="adb reboot bootloader",
    )

    BOOT_TO_MAGISK_IMAGE = TaskOperationContainer(
        index=4,
        title="Boot to Magisk Image",
        description="💾 Flashing the patched Magisk image with fastboot.",
    )


def main():
    pass


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260203
