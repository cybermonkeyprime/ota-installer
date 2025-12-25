# src/ota_installer/images/magisk_image/containers/magisk_image_tuple.py
from collections import namedtuple

MagiskImageTuple = namedtuple(
    "MagiskImageStruct", ["local_path", "remote_path"]
)
