# src/ota_installer/tasks/operations/task_operation_details.py
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True, slots=True)
class TaskOperation(object):
    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None


class TaskOperationDetails(Enum):
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


class _TaskOperationDetails(Enum):
    EXTRACT_PAYLOAD_IMAGE = Enum(
        "01",
        {
            "INDEX": 1,
            "TITLE": "Payload Image Extractor",
            "DESCRIPTION": "📦 Extracting payload.bin to access OTA image files.",
        },
    )
    RENAME_PAYLOAD_IMAGE = Enum(
        "02",
        {
            "INDEX": 2,
            "TITLE": "Payload Image Renamer",
            "DESCRIPTION": "📝 Renaming the extracted image file for clarity.",
        },
    )
    EXTRACT_STOCK_BOOT_IMAGE = Enum(
        "03",
        {
            "INDEX": 3,
            "TITLE": "Boot Image Extractor",
            "DESCRIPTION": "🪄  Pulling the boot image from the OTA payload.",
        },
    )
    BACKUP_STOCK_BOOT_IMAGE = Enum(
        "04",
        {
            "INDEX": 4,
            "TITLE": "Backup Stock Boot Image",
            "DESCRIPTION": "📁 Backing up your stock boot image.",
        },
    )
    CHECK_ADB_CONNECTION = Enum(
        "05",
        {
            "INDEX": 1,
            "TITLE": "Check ADB Connection",
            "DESCRIPTION": "🔌 Checking for an ADB-connected device.",
            "COMMAND_STRING": "adb devices",
        },
    )
    PUSH_STOCK_BOOT_IMAGE = Enum(
        "06",
        {
            "INDEX": 2,
            "TITLE": "Push Stock Boot Image",
            "DESCRIPTION": "📤 Pushing the stock boot image to your device.",
            "REMINDER": "Patch boot image in Magisk app",
        },
    )
    FIND_MAGISK_IMAGE = Enum(
        "07",
        {
            "INDEX": 3,
            "TITLE": "Find Magisk Image",
            "DESCRIPTION": "🔍 Searching for the patched Magisk image.",
        },
    )
    PULL_MAGISK_IMAGE = Enum(
        "08",
        {
            "INDEX": 4,
            "TITLE": "Pull Magisk Image",
            "DESCRIPTION": "📥 Pulling the patched Magisk image to your computer.",
        },
    )

    REBOOT_TO_RECOVERY = Enum(
        "09",
        {
            "INDEX": 1,
            "TITLE": "Reboot To Recovery",
            "DESCRIPTION": "♻️ Rebooting the device into recovery mode.",
            "COMMAND_STRING": "adb reboot recovery",
        },
    )

    APPLY_OTA_UPDATE = Enum(
        "10",
        {
            "INDEX": 2,
            "TITLE": "Apply OTA Image",
            "DESCRIPTION": "🚀 Applying the OTA update via adb sideload.",
            "REMINDER": "Restart to verify build, then reboot to Bootloader",
        },
    )
    REBOOT_TO_BOOTLOADER = Enum(
        "11",
        {
            "INDEX": 3,
            "TITLE": "Reboot to Bootloader",
            "DESCRIPTION": "🧰 Rebooting into bootloader (fastboot) mode.",
            "COMMAND_STRING": "adb reboot bootloader",
        },
    )

    BOOT_TO_MAGISK_IMAGE = Enum(
        "12",
        {
            "INDEX": 4,
            "TITLE": "Boot to Magisk Image",
            "DESCRIPTION": "💾 Flashing the patched Magisk image with fastboot.",
        },
    )


def main():
    pass


if __name__ == "__main__":
    main()
