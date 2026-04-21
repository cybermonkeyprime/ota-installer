# src/ota_installer/dispatchers/factories/dispatch_retriever.py
from dataclasses import dataclass
from typing import Self

from ..constants.dispatcher_type import DispatcherType


@dataclass
class DispatchRetriever(object):
    """
    Handles safe lookup and validation of dispatcher types from string keys.
    Backed by DispatcherType enum. Returns plugin dispatcher classes.
    """

    process_type: str

    def set_function_call(self, function_call) -> Self:
        """Sets the function call for the dispatcher."""
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> type | None:
        """Retrieves the dispatcher class based on the process type."""
        return DispatcherType.retrieve_dispatcher(
            self.process_type, self.function_call
        )
