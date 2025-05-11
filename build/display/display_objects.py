from dataclasses import dataclass, field

import build.display.components as dc


@dataclass
class DisplayObjectDefinitions(object):
    display_title: str = field(default="OTA-Installer")

    @property
    def display_objects(self) -> "dict[str,DisplayObjectAttributes]":
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
class DisplayObjectProcessor(object):
    object_title: str = field(default="")
    display_title: str = field(default="OTA-Installer")

    @property
    def display_objects(self) -> "dict[str,DisplayObjectAttributes]":
        display_object_definitions = DisplayObjectDefinitions()
        return display_object_definitions.display_objects

    def get_object_values(self, key: str) -> "DisplayObjectAttributes | str":
        return self.display_objects.get(key, "Invalid Key")

    def process_object(self) -> "type":
        obj = self.get_object_values(self.object_title)

        object_attribute_processor = DisplayObjectAttributeProcessor(obj)
        return object_attribute_processor.process_object_attributes()


@dataclass
class DisplayObjectAttributeProcessor(object):
    object_attributes: "DisplayObjectAttributes | str"

    @property
    def class_object(self) -> type:
        return self.object_attributes._type

    @property
    def class_arguments(self) -> str | None:
        return self.object_attributes.argument

    def process_object_attributes(self):
        if self.class_arguments:
            return self.process_object_attributes_with_arguments()
        else:
            return self.process_object_attributes_without_arguments()

    def process_object_attributes_with_arguments(self) -> type:
        return self.class_object(self.class_arguments)

    def process_object_attributes_without_arguments(self) -> type:
        return self.class_object()


@dataclass
class DisplayObjectAttributes(object):
    _type: type
    argument: str | None
