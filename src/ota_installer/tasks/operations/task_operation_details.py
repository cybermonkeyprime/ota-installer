# src/tasks/operations/task_operation_details.py
from enum import Enum


class TaskOperationDetails(Enum):
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
