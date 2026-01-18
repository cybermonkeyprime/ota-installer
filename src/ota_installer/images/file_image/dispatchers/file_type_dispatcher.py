# src/ota_installer/images/file_image/dispatchers/file_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ....dispatchers.templates.dispatcher_template import DispatcherTemplate
from ....images.file_image.constants.file_image_names import FileImageNames


@dispatcher_plugin(DispatcherConstants.FILE.value)
@dataclass
class FileTypeDispatcher(DispatcherTemplate):
    """
    Dispatcher for handling file types based on a collection of file paths.
    """

    obj: type = field(default_factory=lambda: type)
    collection: dict[str, Path] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """
        Initializes the collection with normalized keys and corresponding
        file paths.
        """
        self.collection = {
            self.normalize_key(enum_member.name): getattr(
                self.obj.file_paths, enum_member.value
            )
            for enum_member in FileImageNames
        }


# Signed off by Brian Sanford on 20260118
