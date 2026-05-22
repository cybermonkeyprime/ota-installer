from dataclasses import dataclass, field
from functools import singledispatchmethod
from pathlib import Path
from typing import Self

from ....dispatcher.dispatcher_info import DispatcherType
from ....variable.variable_manager import VariableManager
from ...variable.processor.base_process_handler import BaseProcessor
from ..variable_item_handler import VariableItemContainer, VariableTableBuilder


@dataclass(frozen=True, slots=True)
class VariableItemSpec:
    title: str
    key: str
    path_name_only: bool = False


@dataclass(slots=True)
class VariableItemProcessor(BaseProcessor):
    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    items: tuple[VariableItemSpec, ...] = field(default_factory=tuple)
    leading_newline: bool = False
    type: str = field(init=False)

    def __post_init__(self) -> None:
        self.dispatcher_type = DispatcherType[self.type.upper()].value
        super().__post_init__()

    @singledispatchmethod
    def set_items(self, value) -> Self:
        raise TypeError(f"Unsupported item type: {type(value)!r}")

    @set_items.register
    def _(self, value: str) -> Self:
        self.items = (VariableItemSpec(title=value, key=value),)
        return self

    @set_items.register
    def _(self, value: tuple) -> Self:
        self.items = tuple(self._coerce_item(item) for item in value)
        return self

    def set_item(self, title: str, key: str) -> Self:
        self.items = (VariableItemSpec(title=title, key=key),)
        return self

    def with_leading_newline(self) -> Self:
        self.leading_newline = True
        return self

    def _coerce_item(
        self, item: str | tuple[str, str] | VariableItemSpec
    ) -> VariableItemSpec:
        match item:
            case VariableItemSpec():
                return item
            case str():
                return VariableItemSpec(title=item, key=item)
            case (title, key):
                return VariableItemSpec(title=str(title), key=str(key))
            case _:
                raise TypeError(f"Invalid variable item: {item!r}")

    def process_items(self) -> Self:
        builder = VariableTableBuilder(indent=3)

        if self.leading_newline:
            builder.newline()

        for item in self.items:
            value = str(self.get_value_by_key(item.key))
            if item.path_name_only:
                value = Path(value).name

            data = VariableItemContainer(title=item.title, value=value)
            builder.add(data.title, data.value)

        builder.render()
        return self
