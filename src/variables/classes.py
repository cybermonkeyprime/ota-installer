# src/variables/classes.py
from dataclasses import dataclass
from typing import Self

import src.dispatchers as dispatchers

from .constants import DispatcherTypes


@dataclass
class DispatcherRetriever(object):
    process_type: str

    def allowed_dispatchers(self) -> tuple:
        return tuple(enum.value for enum in DispatcherTypes)

    def set_function_call(self, function_call) -> Self:
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> dispatchers.DispatcherInterface | None:
        if self.process_type in self.allowed_dispatchers():
            return (
                dispatchers.DispatcherInterface(
                    self.process_type, self.function_call
                )
                or None
            )
