# src/ota_installer/tasks/mappings/bindings.py
from ..components.t01_payload_image_extractor import (
    PayloadImageExtractor,
)
from ..components.t02_payload_image_renamer import PayloadImageRenamer
from ..components.t03_boot_image_extractor import BootImageExtractor
from ..components.t04_stock_boot_image_backupper import (
    StockBootImageBackupper,
)
from ..components.t05_adb_connection_checker import (
    ADBConnectionChecker,
)
from ..components.t06_stock_boot_image_pusher import (
    StockBootImagePusher,
)
from ..components.t07_magisk_image_finder import MagiskImageFinder
from ..components.t08_magisk_image_puller import MagiskImagePuller
from ..components.t09_recovery_rebooter import RecoveryRebooter
from ..components.t10_apply_ota_update import ADBSideloader
from ..components.t11_bootloader_rebooter import BootloaderRebooter
from ..components.t12_magisk_image_booter import MagiskImageBooter
from .constants import (
    ApplicationTasks,
    MigrationTasks,
    PreparationTasks,
)

TASK_CLASS_MAP = {
    PreparationTasks.EXTRACT_PAYLOAD_IMAGE.name: PayloadImageExtractor,
    PreparationTasks.RENAME_PAYLOAD_IMAGE.name: PayloadImageRenamer,
    PreparationTasks.EXTRACT_STOCK_BOOT_IMAGE.name: BootImageExtractor,
    PreparationTasks.BACKUP_STOCK_BOOT_IMAGE.name: StockBootImageBackupper,
    MigrationTasks.CHECK_ADB_CONNECTION: ADBConnectionChecker,
    MigrationTasks.PUSH_STOCK_BOOT_IMAGE: StockBootImagePusher,
    MigrationTasks.FIND_PATCHED_BOOT_IMAGE: MagiskImageFinder,
    MigrationTasks.PULL_PATCHED_BOOT_IMAGE: MagiskImagePuller,
    ApplicationTasks.REBOOT_TO_RECOVERY: RecoveryRebooter,
    ApplicationTasks.APPLY_OTA_UPDATE: ADBSideloader,
    ApplicationTasks.REBOOT_TO_BOOTLOADER: BootloaderRebooter,
    ApplicationTasks.BOOT_TO_MAGISK_IMAGE: MagiskImageBooter,
}
