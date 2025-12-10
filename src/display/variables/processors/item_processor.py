# src/display/variables/processors/item_processor.py
from dataclasses import dataclass
from typing import Self

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
        from ..classes import VariableTableBuilder

        try:
            builder = VariableTableBuilder(indent=3)
            if self.enum_title == "log_file":
                builder.add("[dim]", "")  # Subtle, clean break
            builder.add(self.enum_title.upper(), self.enum_value)
            builder.render()
        except AttributeError as error:
            logger.error(
                f"Processing {self.item_title.capitalize()}"
                f"{self.item_name} failed: "
                f"{type(error).__name__} {error}"
            )
        return self
