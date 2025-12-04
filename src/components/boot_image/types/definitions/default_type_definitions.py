from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

import src.structures as structures

T = TypeVar("T", "PayloadImage", "StockImage", "MagiskImage")


class AbstractImageTemplate(ABC):
    @abstractmethod
    def generate_file_name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def generate_directory(self) -> str:
        raise NotImplementedError()


@dataclass
class PayloadImage(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-payload-{self.version}.bin"

    def generate_directory(self) -> str:
        return ""


@dataclass
class StockImage(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-boot-{self.version}.img"

    def generate_directory(self) -> str:
        return f"{self.path}/stock"


@dataclass
class MagiskImage(AbstractImageTemplate):
    device: str = field(default="")
    version: str = field(default="")
    path: str = field(default="")

    def generate_file_name(self) -> str:
        return f"{self.device}-magisk-{self.version}.img"

    def generate_directory(self) -> str:
        return f"{self.path}/magisk"


@dataclass
class DefaultTypeDefinition:
    file_name_parser: structures.FileNameParser

    path: str = field(default="")
    payload_image: structures.ImageFile = field(init=False)
    stock_image: structures.ImageFile = field(init=False)
    magisk_image: structures.ImageFile = field(init=False)

    def __post_init__(self) -> None:
        self.payload = self.create_image_file(PayloadImage)
        self.stock = self.create_image_file(StockImage)
        self.magisk = self.create_image_file(MagiskImage)

    def create_image_file(
        self,
        image_template_class: type[T],
    ) -> structures.ImageFile:
        device = self.file_name_parser.device
        version = self.file_name_parser.version
        try:
            image_instance = image_template_class(device, version, self.path)
            return structures.ImageFile(
                Path(image_instance.generate_file_name()),
                Path(image_instance.generate_directory()),
            )
        except Exception as e:
            raise ValueError("Failed to create image structure: ") from e


def create_file_name_parser(variable: str) -> structures.FileNameParser:
    return structures.FileNameParser(variable)


if __name__ == "__main__":
    variable = "example_device-2.0"
    parser = create_file_name_parser(variable)
    image_manager = DefaultTypeDefinition(parser)
    print(image_manager.payload_image)
    print(image_manager.stock_image)
    print(image_manager.magisk_image)
    pass
