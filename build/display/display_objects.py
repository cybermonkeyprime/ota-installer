from dataclasses import dataclass, field

import build.display.components as dc

DisplayObjectDictionary = dict[str, "DisplayObjectAttributes"]


@dataclass
class DisplayObjectDefinitions(object):
    """
    Class for defining display object attributes.

    Attributes:
        display_title (str): The title to be displayed. Defaults to
            "OTA-Installer".
    """

    display_title: str = field(default="OTA-Installer")

    @property
    def display_objects(self) -> DisplayObjectDictionary:
        """
        Property that returns a dictionary of display object attributes.

        Returns:
            DisplayObjectDictionary: A dictionary with keys as display
                object names and values as `DisplayObjectAttributes`.
        """
        return {
            "display_title": DisplayObjectAttributes(
                dc.DisplayTitle, self.display_title
            ),
            "display_separator": DisplayObjectAttributes(
                dc.DisplaySeparator, None
            ),
            "display_versioning": DisplayObjectAttributes(
                dc.DisplaySubtitle, None
            ),
        }


@dataclass
class DisplayObjectGetter(object):
    """
    Class for getting display object definitions.

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
            DisplayObjectDictionary: A dictionary of display objects.
        """
        return self.display_object_definitions.display_objects


@dataclass
class DisplayObjectProcessor(object):
    """
    Class for processing display objects.

    Attributes:
        object_title (str): The title of the object to process.
        display_title (str): The title to be displayed. Defaults to
            "OTA-Installer".
        display_object_getter (DisplayObjectGetter): The getter for
            display objects.
    """

    object_title: str = field(default="")
    display_title: str = field(default="OTA-Installer")
    display_object_getter: "DisplayObjectGetter" = field(
        default_factory=DisplayObjectGetter
    )

    def __post_init__(self) -> None:
        """
        Post-initialization method to set up display objects.
        """
        self.display_objects = self.display_object_getter.get_display_objects()

    def get_object_values(self, key: str) -> "DisplayObjectAttributes | str":
        """
        Method to get the value of a display object by key.

        Args:
            key (str): The key of the display object.

        Returns:
            DisplayObjectAttributes | str: The attributes of the display object
                or "Invalid Key" if not found.
        """
        return self.display_objects.get(key, "Invalid Key")

    def process_object(self) -> str | type:
        """
        Method to process the display object based on the object title.

        Returns:
            str | type: The processed object or the type of the object.
        """
        obj = self.get_object_values(self.object_title)

        object_attribute_processor = DisplayObjectAttributeProcessor(obj)
        return object_attribute_processor.process_object_attributes()


@dataclass
class DisplayObjectAttributeProcessor(object):
    """
    Class for processing attributes of a display object.

    Attributes:
        object_attributes (DisplayObjectAttributes | str): The attributes of
            the display object.
    """

    object_attributes: "DisplayObjectAttributes | str"
    class_object: type = field(init=False)
    class_arguments: str | None = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method to set up class object and arguments.
        """
        self.class_object = self.object_attributes._type
        self.class_arguments = self.object_attributes.argument

    def process_object_attributes(self):
        """
        Method to process object attributes with or without arguments.

        Returns:
            The processed object.
        """
        if self.class_arguments:
            return self.process_object_attributes_with_arguments()
        else:
            return self.process_object_attributes_without_arguments()

    def process_object_attributes_with_arguments(self) -> str:
        return self.class_object(self.class_arguments)

    def process_object_attributes_without_arguments(self) -> type:
        return self.class_object()


@dataclass
class DisplayObjectAttributes(object):
    """
    Data class for holding display object attributes.

    Attributes:
        _type (type): The type of the display object.
        argument (str | None): The argument for the display object, if any.
    """

    _type: type
    argument: str | None


def main() -> None:
    """
    Main function to execute the program.
    """
    pass


if __name__ == "__main__":
    main()
