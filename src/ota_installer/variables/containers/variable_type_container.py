# src/ota_installer/variables/containers/variable_type_container.py
from collections import namedtuple

VariableTypeContainer = namedtuple(
    "VariableTypeTuple",
    ["file_path", "magisk_image_name", "file_path_stem", "file_parts"],
)
