from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ..dispatcher.dispatcher_template import DispatcherTemplate
from ..dispatcher.dispatcher_type import DispatcherType
from ..plugin.plugin_registry import Plugin
from .image_name import ImageName


@Plugin.DISPATCHER.register(name=DispatcherType.FILE.value)
@dataclass
class FileTypeDispatcher(DispatcherTemplate):
    """
    Dispatcher for handling file types based on a collection of file paths.
    """

    obj: type = field(default_factory=lambda: type)
    collection: Mapping[str, Path] = field(init=False, default_factory=dict)

    def __post_init__(self) -> None:
        """
        Initializes the collection with normalized keys and corresponding
        file paths.
        """
        self.collection = ImageName.create_path_dictionary(self.obj.file_paths)
