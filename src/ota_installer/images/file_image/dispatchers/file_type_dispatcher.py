# src/ota_installer/images/file_image/dispatchers/file_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, TypeVar

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ....dispatchers.templates.dispatcher_creator import DispatcherCreator
from ....images.file_image.constants.file_image_names import FileImageNames

T = TypeVar("T")


CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]
CollectionEnum = Literal


@dispatcher_plugin(DispatcherConstants.FILE.value)
@dataclass
class FileTypeDispatcher(object):
    obj: type = field(default_factory=lambda: type)

    collection: dict = field(init=False, default_factory=dict)
    """
    A File dispatcher class for dispatching tasks based on a key-value
    collection.
    """

    def __post_init__(self) -> None:
        self.collection = {
            enum_member.name: self.obj.file_paths.get(enum_member.value)
            for enum_member in FileImageNames
        }

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """
        return self.collection[key.upper()]

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """
        return (
            DispatcherCreator()
            .set_collection(self.collection)
            .get_instance(key)
        )
