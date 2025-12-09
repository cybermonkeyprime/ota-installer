from dataclasses import dataclass, field
from pathlib import Path

import src.structures as structures
import src.types.boot_image as boot_image


# Centralized manager
@dataclass
class DefaultImageTypeManager(object):
    file_name_bits: structures.FileNameParser
    path: str = field(default="")

    payload_image: structures.ImageFile = field(init=False)
    stock_image: structures.ImageFile = field(init=False)
    magisk_image: structures.ImageFile = field(init=False)

    def __post_init__(self):
        self.device = self.file_name_bits.device
        self.version = self.file_name_bits.version

        self.payload = self.create_image("payload", "bin")
        self.stock = self.create_image("boot", "img")
        self.magisk = self.create_image("magisk", "img")

    def create_image(self, title: str, ext: str) -> structures.ImageFile:
        manager = boot_image.DynamicImageTypeManager(
            device=self.device,
            version=self.version,
            path=self.path,
            title=title,
            extension=ext,
        )
        return structures.ImageFile(
            Path(str(manager.generate_file_name())),
            Path(manager.generate_directory()),
        )


# Optional test function
def create_file_name_parser(variable: Path) -> structures.FileNameParser:
    return structures.FileNameParser(variable)


if __name__ == "__main__":
    variable = Path("pixelpro-global-2.0")
    parser = create_file_name_parser(variable)
    manager = DefaultImageTypeManager(parser, path="")

    print(manager.payload_image)
    print(manager.stock_image)
    print(manager.magisk_image)
