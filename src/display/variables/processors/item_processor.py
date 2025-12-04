# src/display/variables/processors/item_processor.py
from dataclasses import dataclass
from typing import Self

import src.display.variables.classes as classes
from src.logger import logger


@dataclass
class ItemProcessor(object):
    def set_item_title(self, item_name: str) -> Self:
        self.item_title = str(item_name)
        return self

    def set_item_name(self, item_name: str) -> Self:
        self.item_name = str(item_name)
        return self

    def set_enum_title(self, enum_name: str) -> Self:
        self.enum_title = str(enum_name)
        return self

    def set_enum_value(self, enum_value: str) -> Self:
        self.enum_value = str(enum_value)
        return self

    def process_item(self) -> Self:
        try:
            (
                classes.EnumBuilder()
                .set_title(self.enum_title)
                .set_value(self.enum_value)
                .set_data_enum()
                .show_output()
            )
        except AttributeError as error:
            logger.error(
                f"Processing {self.item_title.capitalize()}"
                f"{self.item_name} failed: "
                f"{type(error).__name__} {error}"
            )
        return self
