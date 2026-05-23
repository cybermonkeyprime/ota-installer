# src/ota_installer/plugin/loader/task_plugin_loader.py
from ...task.component import (
    t01_payload_image_extractor,
    t02_payload_image_renamer,
    t03_boot_image_extractor,
    t04_stock_boot_image_backupper,
    t05_adb_connection_checker,
    t06_stock_boot_image_pusher,
    t07_magisk_image_finder,
    t08_magisk_image_puller,
    t09_recovery_rebooter,
    t10_apply_ota_update,
    t11_bootloader_rebooter,
    t12_magisk_image_booter,
)

# Signed off by Brian Sanford on 20260523
