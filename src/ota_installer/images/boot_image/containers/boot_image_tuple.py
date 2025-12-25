# src/ota_installer/images/boot_image/containers/boot_image_tuple.py
from collections import namedtuple

BootImageTuple = namedtuple("BootImageContainer", ["stock", "magisk"])

# data = BootImageContainer(*boot_image_paths)
