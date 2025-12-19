# src/ota_installer/tasks/constants/preparation_task_constants.py
from enum import Enum


class PreparationTaskConstants(Enum):
    EXTRACT_PAYLOAD_IMAGE = "extract_payload_image"
    RENAME_PAYLOAD_IMAGE = "rename_payload_image"
    EXTRACT_STOCK_BOOT_IMAGE = "extract_stock_boot_image"
    BACKUP_STOCK_BOOT_IMAGE = "backup_stock_boot_image"
