# src/ota_installer/tasks/constants/application_task_constants.py
from enum import Enum


class ApplicationTaskConstants(Enum):
    REBOOT_TO_RECOVERY = "reboot_to_recovery"
    APPLY_OTA_UPDATE = "apply_ota_update"
    REBOOT_TO_BOOTLOADER = "reboot_to_bootloader"
    BOOT_TO_MAGISK_IMAGE = "boot_to_magisk_image"
