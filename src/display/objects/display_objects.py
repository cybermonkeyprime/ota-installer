# src/display/objects/display_objects.py
from dataclasses import dataclass
from enum import Enum
from functools import singledispatchmethod
from typing import NamedTuple

import src.display.components as dc


# Type alias for better readability
class DisplayObjectTuple(NamedTuple):
    """
    NamedTuple to represent a display object with its associated metadata.
    """

    object_name: str
    class_name: type
    class_argument: str | None


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


# Enums for better readability and maintainability
class DisplayObjectTypes(Enum):
    """Enum representing different types of display objects."""

    TITLE = DisplayObjectTuple("title", dc.DisplayTitle, "OTA-Installer")
    SEPARATOR = DisplayObjectTuple("separator", dc.DisplaySeparator, None)
    SUBTITLE = DisplayObjectTuple("subtitle", dc.DisplaySubtitle, None)

    def __str__(self) -> str:
        """String representation of the DisplayObjectTypes enum."""

        return self.value.object_name

    @property
    def processor(self):
        """Property to process the associated display object."""

        processor = DisplayObjectProcessor(self.value.class_name)
        return processor.process_object(self.value.class_argument)


def main():
    print(DisplayObjectTypes.TITLE.processor)
    print(DisplayObjectTypes.SEPARATOR.processor)
    print(DisplayObjectTypes.SUBTITLE.processor)


if __name__ == "__main__":
    main()
