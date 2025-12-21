# src/ota_installer/tasks/constants/bindings.py
from enum import Enum

from ...task_groups.constants import (
    ApplicationTasks,
    MigrationTasks,
    PreparationTasks,
)
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

Preparation = PreparationTasks

TASK_CLASS_MAP = {
    PreparationTasks.EXTRACT_PAYLOAD_IMAGE.lower_case: PreparationTasks.EXTRACT_PAYLOAD_IMAGE.Class,
    PreparationTasks.RENAME_PAYLOAD_IMAGE.lower_case: PayloadImageRenamer,
    PreparationTasks.EXTRACT_STOCK_BOOT_IMAGE.name: BootImageExtractor,
    PreparationTasks.BACKUP_STOCK_BOOT_IMAGE.name: StockBootImageBackupper,
    MigrationTasks.CHECK_ADB_CONNECTION.name: ADBConnectionChecker,
    MigrationTasks.PUSH_STOCK_BOOT_IMAGE.name: StockBootImagePusher,
    MigrationTasks.FIND_PATCHED_BOOT_IMAGE.name: MagiskImageFinder,
    MigrationTasks.PULL_PATCHED_BOOT_IMAGE.name: MagiskImagePuller,
    ApplicationTasks.REBOOT_TO_RECOVERY.name: RecoveryRebooter,
    ApplicationTasks.APPLY_OTA_UPDATE.name: ADBSideloader,
    ApplicationTasks.REBOOT_TO_BOOTLOADER.name: BootloaderRebooter,
    ApplicationTasks.BOOT_TO_MAGISK_IMAGE.name: MagiskImageBooter,
}


class TaskClassMap(Enum):
    """preparation"""

    EXTRACT_PAYLOAD_IMAGE = PreparationTasks.EXTRACT_PAYLOAD_IMAGE.Class
    RENAME_PAYLOAD_IMAGE = PayloadImageRenamer
    EXTRACT_STOCK_BOOT_IMAGE = BootImageExtractor
    BACKUP_STOCK_BOOT_IMAGE = StockBootImageBackupper
    """ migration"""

    CHECK_ADB_CONNECTION = ADBConnectionChecker
    PUSH_STOCK_BOOT_IMAGE = StockBootImagePusher
    FIND_PATCHED_BOOT_IMAGE = MagiskImageFinder
    PULL_PATCHED_BOOT_IMAGE = MagiskImagePuller
    """ application"""

    REBOOT_TO_RECOVERY = RecoveryRebooter
    APPLY_OTA_UPDATE = ADBSideloader
    REBOOT_TO_BOOTLOADER = BootloaderRebooter
    BOOT_TO_MAGISK_IMAGE = MagiskImageBooter
