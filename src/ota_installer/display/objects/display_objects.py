# src/ota_installer/display/objects/display_objects.py
from dataclasses import dataclass
from functools import singledispatchmethod

from .constants.display_object_function_calls import DisplayObjectFunctionCalls


@dataclass
class DisplayObjectProcessor(object):
    """
    Processor class for creating display objects based on the provided
        class type and argument.
    """

    class_name: type

    @singledispatchmethod
    def process_object(self, argument):
        """Default method for processing an object with an unsupported type."""

        return f"Unsupported type: {type(argument).__name__})"

    @process_object.register
    def _(self, argument: None):
        """Process an object when the argument is None"""

        return self.class_name()

    @process_object.register
    def _(self, argument: str):
        """Process an object when the argument is an string."""

        return self.class_name(argument)

    @process_object.register
    def _(self, argument: object):
        """Process an object when the argument is an object."""

        return self.class_name(argument)


def main():
    function_calls = DisplayObjectFunctionCalls
    print(function_calls.TITLE.processor)
    print(function_calls.SEPARATOR.processor)
    print(function_calls.SUBTITLE.processor)


if __name__ == "__main__":
    main()
