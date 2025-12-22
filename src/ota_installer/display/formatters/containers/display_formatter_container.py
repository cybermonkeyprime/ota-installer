# src/ota_installer/display/formatters/containers/display_formatter_container.py
from collections import namedtuple

DisplayFormatterContainer = namedtuple(
    "DisplayFormatterContainer",
    ["title", "major_number", "minor_number", "patch_number"],
)
