from dataclasses import dataclass

import src.types.boot_image as boot_image


# Dynamic manager for all image types
@dataclass
class DynamicImageTypeManager(object):
    device: str
    version: str
    path: str
    title: str
    extension: str

    def __post_init__(self):
        self.creator = (
            boot_image.ImageCreator()
            .set_device(self.device)
            .set_version(self.version)
            .set_path(self.path)
            .set_file_name(self.title)
            .set_extension(self.extension)
        )

    def generate_file_name(self) -> str | None:
        return self.creator.generate_file_name()

    def generate_directory(self) -> str:
        return self.creator.generate_directory()
