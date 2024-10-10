from dataclasses import dataclass
from typing import Optional
from build.structures import FileNameParser

import build.types.definitions as definitions


@dataclass
class ImageFile(object):
    filename_parser: FileNameParser
    boot_image_directory: str

    def create_image(self) -> Optional[definitions.ImageFile]:
        try:
            return definitions.ImageFile(
                self.filename_parser, self.boot_image_directory
            )
        except Exception as e:
            print(f"{e}")
            return None
