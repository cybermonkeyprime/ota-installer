from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Magisk:
    local_path: Path = field(
        default_factory=lambda: Path.home() / "Android" / "boot-images" / "magisk"
    )
    remote_path: Path = field(default_factory=lambda: Path("/sdcard/Download/magisk"))
