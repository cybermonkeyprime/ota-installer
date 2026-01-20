# src/ota_installer/images/magisk_image/containers/magisk_image_tuple.py
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MagiskImageTuple(object):
    """Represents a Magisk image with local and remote paths."""

    local_path: Path
    remote_path: Path


# Signed off by Brian Sanford on 20260120
