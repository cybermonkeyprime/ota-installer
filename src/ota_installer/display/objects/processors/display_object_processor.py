# src/ota_installer/display/objects/processors/display_object_processor.py
from dataclasses import dataclass
from functools import singledispatchmethod


@dataclass
class DisplayObjectProcessor(object):
    """
    Processor class for creating display objects based on the provided
        function type and argument.
    """

    function: type

    @singledispatchmethod
    def process_object(self, argument):
        """Default method for processing an object with an unsupported type."""

        return f"Unsupported type: {type(argument).__name__})"

    @process_object.register
    def _(self, argument: None):
        """Process an object when the argument is None"""

        return self.function()

    @process_object.register
    def _(self, argument: str):
        """Process an object when the argument is an string."""

        return self.function(argument)

    @process_object.register
    def _(self, argument: object):
        """Process an object when the argument is an object."""

        return self.function(argument)


def main():
    pass


if __name__ == "__main__":
    main()
