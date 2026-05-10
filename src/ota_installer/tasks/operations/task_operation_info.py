# tasks/operations/task_operation_info.py
from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum, auto


class Styles(StrEnum):
    """Constants for styles."""

    COMMAND = "non_error"
    NON_ERROR = auto()
    WARNING = auto()
    TASK = auto()
    DESCRIPTION = "warning"


class Indents(IntEnum):
    """Constants for indents."""

    COMMAND = 3
    DESCRIPTION = 3
    EXECUTE = 3
    REMINDER = 2
    KEYPRESS = 1


class Messages(Enum):
    """Constants for messages."""

    EXECUTE = "execute the task"


class DefaultIndent(IntEnum):
    """Constants for default indent properties."""

    SPACING = 4
    INTERVAL = 1


class TaskOpsItemType(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str

    @classmethod
    def get_validated_type(cls, field_name: str) -> type:
        """
        Validates field existence using a whitelist check.
        Raises AttributeError immediately on failure (Fail-Fast).
        """
        key: str = field_name.upper()

        # Explicit membership check: 'Look Before You Leap'
        if not key:
            raise AttributeError(
                f"Invalid field: '{field_name}'. "
                f"Allowed fields are: {', '.join(cls._member_names_)}"
            ) from None

        return cls[key].value


@dataclass
class TaskOperationContainer:
    """Container for task operation details."""

    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None


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


# Signed off by Brian Sanford on 20260510
