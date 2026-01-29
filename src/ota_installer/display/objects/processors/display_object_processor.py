# src/ota_installer/display/objects/processors/display_object_processor.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import singledispatchmethod


@dataclass
class DisplayObjectProcessor(object):
    """
    Processor class for creating display objects based on the provided
        callable and argument.
    """

    function: Callable

    @singledispatchmethod
    def process_object(self, argument: str | None | object) -> str:
        """Process the provided argument using a callable."""
        raise ValueError(f"Unsupported type: {type(argument).__name__}")

    @process_object.register
    def _(self, argument: None) -> str:
        """Process the argument when it is None."""
        return self.function()

    @process_object.register
    def _(self, argument: str) -> str:
        """Process the argument when it is a string."""
        return self.function(argument)


def main():
    pass


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260129
