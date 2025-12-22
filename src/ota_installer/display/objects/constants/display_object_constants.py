# src/ota_installer/display/objects/constants/display_object_constants.py
from enum import Enum

from ...components import DisplaySeparator, DisplaySubtitle, DisplayTitle
from ..containers.display_object_container import DisplayObjectContainer
from ..processors.display_object_processor import DisplayObjectProcessor


# Enums for better readability and maintainability
class DisplayObjectConstants(Enum):
    """Enum representing different types of display objects."""

    TITLE = DisplayObjectContainer("title", DisplayTitle, "OTA-Installer")
    SEPARATOR = DisplayObjectContainer("separator", DisplaySeparator, None)
    SUBTITLE = DisplayObjectContainer("subtitle", DisplaySubtitle, None)

    def __str__(self) -> str:
        """String representation of the DisplayObjectTypes enum."""

        return self.value.object_name

    @property
    def processor(self):
        """Property to process the associated display object."""

        processor = DisplayObjectProcessor(self.value.class_name)
        return processor.process_object(self.value.class_argument)


def main():
    print(DisplayObjectConstants.TITLE.processor)
    print(DisplayObjectConstants.SEPARATOR.processor)
    print(DisplayObjectConstants.SUBTITLE.processor)


if __name__ == "__main__":
    main()
