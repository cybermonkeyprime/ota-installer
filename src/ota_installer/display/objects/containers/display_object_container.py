# src/ota_installer/display/objects/containers/display_object_container.py
from collections import namedtuple

DisplayObjectContainer = namedtuple(
    "DisplayObjectContainer",
    ["object_name", "function"],
)
