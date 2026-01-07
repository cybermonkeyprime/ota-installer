# src/ota_installer/variables/containers/file_name_container.py
from collections import namedtuple

FileNameContainer = namedtuple(
    "FileNameParts", ["device", "file_type", "version", "extra"]
)
