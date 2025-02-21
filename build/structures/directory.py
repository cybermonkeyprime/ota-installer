from dataclasses import dataclass, field
from build.structures.boot_image import BootImage
from build.structures.magisk import Magisk


@dataclass
class Directory:
    ota: str
    _boot_image: str = field(repr=False)
    boot_image: BootImage = field(init=False)
    magisk: Magisk = field(init=False)

    def __post_init__(self) -> None:
        self.boot_image = BootImage(self._boot_image)
        self.magisk = Magisk()

    def __str__(self) -> str:
        return self._boot_image
