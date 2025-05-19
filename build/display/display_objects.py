from dataclasses import dataclass, field

import build.display.components as dc
from build.display.display_object_types import DisplayObjectType

# Type alias for better readability
DisplayObjectDictionary = dict["DisplayObjectType", "DisplayObjectAttributes"]


@dataclass
class DisplayObjectAttributes(object):
    """
    Data class for holding display object attributes.

    Attributes:
        _type (type): The type of the display object.
        argument (str | None): The argument for the display object, if any.
    """

    object_type: type
    argument: str | None


@dataclass
class DisplayObjectDefinitions(object):
    display_title: str = field(default="OTA-Installer")

    @property
    def display_objects(self) -> DisplayObjectDictionary:
        """
        Property that returns a dictionary of display object types to their
            attributes.

        Returns:
            DisplayObjectDictionary: A dictionary mapping display object types
                to their attributes.
        """
        return {
            DisplayObjectType.TITLE: DisplayObjectAttributes(
                dc.DisplayTitle, self.display_title
            ),
            DisplayObjectType.SEPARATOR: DisplayObjectAttributes(
                dc.DisplaySeparator, None
            ),
            DisplayObjectType.SUBTITLE: DisplayObjectAttributes(
                dc.DisplaySubtitle, None
            ),
        }


@dataclass
class DisplayObjectGetter(object):
    """
    Class responsible for getting display object definitions.

    Attributes:
        display_object_definitions (DisplayObjectDefinitions): The definitions
            of display objects.
    """

    display_object_definitions: DisplayObjectDefinitions = field(
        default_factory=DisplayObjectDefinitions
    )

    def get_display_objects(self) -> DisplayObjectDictionary:
        """
        Method to get the display objects from the definitions.

        Returns:
            DisplayObjectDictionary: A dictionary of display object types to
                their attributes.
        """
        return self.display_object_definitions.display_objects


@dataclass
class DisplayObjectProcessor(object):
    """
    Class responsible for processing display objects.

    Attributes:
        display_objects (DisplayObjectDictionary): A dictionary of display
            object types to their attributes.
        display_object_getter (DisplayObjectGetter): An instance of
            DisplayObjectGetter to retrieve display objects.
    """

    display_objects: DisplayObjectDictionary = field(
        default_factory=DisplayObjectDictionary, init=False
    )
    display_object_getter: "DisplayObjectGetter" = field(
        default_factory=DisplayObjectGetter, init=False
    )

    def __post_init__(self) -> None:
        """
        Post-initialization method to set up display objects.
        """
        self.display_objects = self.display_object_getter.get_display_objects()

    def get_object_attributes(
        self, object_type: DisplayObjectType
    ) -> "DisplayObjectAttributes":
        """
        Method to get the attributes of a specific display object type.

        Args:
            object_type (DisplayObjectType): The type of the display object.

        Returns:
            DisplayObjectAttributes: The attributes of the specified display
                object type.

        Raises:
            ValueError: If the object type is invalid.
        """
        try:
            return self.display_objects[object_type]
        except KeyError:
            raise ValueError(f"Invalid object type: {object_type}") from None

    def process_display_object(self, object_type: DisplayObjectType):
        """
        Method to process and return an instance of a display object.

        Args:
            object_type (DisplayObjectType): The type of the display object to
                process.

        Returns:
            An instance of the specified display object type.
        """
        attributes = self.get_object_attributes(object_type)
        if attributes.argument:
            return attributes.object_type(attributes.argument)
        else:
            return attributes.object_type()


def main() -> None:
    """
    Main function to execute the program.
    """
    pass


if __name__ == "__main__":
    main()
