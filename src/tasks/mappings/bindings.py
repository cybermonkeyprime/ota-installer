# src/tasks/mappings/bindings.py
from src.tasks.components.t01_payload_image_extractor import (
    PayloadImageExtractor,
)
from src.tasks.components.t02_payload_image_renamer import PayloadImageRenamer
from src.tasks.components.t03_boot_image_extractor import BootImageExtractor
from src.tasks.components.t04_stock_boot_image_backupper import (
    StockBootImageBackupper,
)
from src.tasks.components.t05_adb_connection_checker import (
    ADBConnectionChecker,
)
from src.tasks.components.t06_stock_boot_image_pusher import (
    StockBootImagePusher,
)
from src.tasks.components.t07_magisk_image_finder import MagiskImageFinder
from src.tasks.components.t08_magisk_image_puller import MagiskImagePuller
from src.tasks.components.t09_recovery_rebooter import RecoveryRebooter
from src.tasks.components.t10_apply_ota_update import ADBSideloader
from src.tasks.components.t11_bootloader_rebooter import BootloaderRebooter
from src.tasks.components.t12_magisk_image_booter import MagiskImageBooter

from .constants import TaskName

TASK_CLASS_MAP = {
    TaskName.EXTRACT_PAYLOAD_IMAGE: PayloadImageExtractor,
    TaskName.RENAME_PAYLOAD_IMAGE: PayloadImageRenamer,
    TaskName.EXTRACT_STOCK_BOOT_IMAGE: BootImageExtractor,
    TaskName.BACKUP_STOCK_BOOT_IMAGE: StockBootImageBackupper,
    TaskName.CHECK_ADB_CONNECTION: ADBConnectionChecker,
    TaskName.PUSH_STOCK_BOOT_IMAGE: StockBootImagePusher,
    TaskName.FIND_PATCHED_BOOT_IMAGE: MagiskImageFinder,
    TaskName.PULL_PATCHED_BOOT_IMAGE: MagiskImagePuller,
    TaskName.REBOOT_TO_RECOVERY: RecoveryRebooter,
    TaskName.ADB_SIDELOAD: ADBSideloader,
    TaskName.REBOOT_TO_BOOTLOADER: BootloaderRebooter,
    TaskName.BOOT_MAGISK_IMAGE: MagiskImageBooter,
}
