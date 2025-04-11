#!/usr/bin/env python3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from build.components.file.structures import FileNameParserStructure
from build.components.boot_image.structures import (
    BootImageFileStructure,
)
from build.components.directory.structures import BootImageDirectoryStructure


class AbstractImageTemplate(ABC):
    @abstractmethod
    def generate_file_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def generate_directory(self) -> str:
        raise NotImplementedError()


@dataclass
class PayloadImageFileNamer(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-payload-{self.version}.bin"

    def generate_directory(self) -> str:
        return ""


@dataclass
class StockImageFileNamer(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-boot-{self.version}.img"

    def generate_directory(self) -> str:
        boot_image_directory = BootImageDirectoryStructure()
        return str(boot_image_directory.stock)


@dataclass
class MagiskImageFileNamer(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-magisk-{self.version}.img"

    def generate_directory(self) -> str:
        boot_image_directory = BootImageDirectoryStructure()
        return str(boot_image_directory.magisk)


@dataclass
class BootImageTypeDefinition(object):
    file_name_parser: type[FileNameParserStructure] = field(
        default_factory=lambda: FileNameParserStructure
    )

    path: str = field(default="")
    payload_image: BootImageDirectoryStructure = field(init=False)
    stock_image: BootImageDirectoryStructure = field(init=False)
    magisk_image: BootImageDirectoryStructure = field(init=False)

    @property
    def payload(self) -> BootImageFileStructure:
        return self.create_image_file(PayloadImageFileNamer)

    @property
    def stock(self) -> BootImageFileStructure:
        return self.create_image_file(StockImageFileNamer)

    @property
    def magisk(self) -> BootImageFileStructure:
        return self.create_image_file(MagiskImageFileNamer)

    def create_image_file(
        self,
        image_template_class: type[
            PayloadImageFileNamer | StockImageFileNamer | MagiskImageFileNamer
        ],
    ) -> BootImageFileStructure:
        device = self.file_name_parser.device
        version = self.file_name_parser.version
        try:
            image_instance = image_template_class(device, version, self.path)
            return BootImageFileStructure(
                image_instance.generate_file_name(),
                image_instance.generate_directory(),
            )
        except Exception as e:
            raise ValueError(f"Failed to create image structure: {e}")


def create_file_name_parser(variable: str) -> FileNameParserStructure:
    return FileNameParserStructure(variable)


if __name__ == "__main__":
    pass
    variable = "example_device-2.0"
    parser = create_file_name_parser(variable)
    # image_manager = BootImageFileStructure(parser)
    # print(image_manager.payload_image)
    # print(image_manager.stock_image)
    # print(image_manager.magisk_image)
