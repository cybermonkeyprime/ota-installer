# src/variables/_classes/dispatch_retriever.py
from dataclasses import dataclass
from typing import Self

from ...dispatchers import DispatcherInterface
from ..constants import DispatcherTypes


@dataclass
class DispatchRetriever(object):
    process_type: str

    def allowed_dispatchers(self) -> tuple:
        return tuple(enum.value for enum in DispatcherTypes)

    def set_function_call(self, function_call) -> Self:
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> DispatcherInterface | None:
        if self.process_type not in self.allowed_dispatchers():
            return None
        return DispatcherInterface(self.process_type, self.function_call)
