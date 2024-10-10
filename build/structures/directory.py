from dataclasses import dataclass, field
from .boot_image import BootImage
from .magisk import Magisk


@dataclass
class Directory:
    ota: str
    # Exclude _boot_image from the generated __repr__
    _boot_image: str = field(repr=False)
    # Exclude boot_image from the __init__ method
    boot_image: BootImage = field(init=False)
    # Exclude magisk from the __init__ method
    magisk: Magisk = field(init=False)

    def __post_init__(self) -> None:
        self.boot_image = BootImage(self._boot_image)
        self.magisk = Magisk()

    def __str__(self) -> str:
        return self._boot_image
