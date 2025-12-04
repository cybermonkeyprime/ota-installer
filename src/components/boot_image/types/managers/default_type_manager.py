from dataclasses import dataclass

from src.structures import FileNameParser

from ..definitions import DefaultTypeDefinition


@dataclass
class DefaultTypeManager(object):
    filename_parser: FileNameParser
    boot_image_directory: str

    def create_image(self) -> DefaultTypeDefinition | None:
        try:
            return DefaultTypeDefinition(
                self.filename_parser, self.boot_image_directory
            )
        except Exception as err:
            print(f"{self}: {err}")
            return None
