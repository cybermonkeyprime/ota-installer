from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

from build.dispatchers import DispatcherMapper, DispatcherTemplate


@dataclass
class DispatcherManager(object):
    """
    Manages the creation and interaction with different types of dispatchers.

    Attributes:
        dispatcher_type: The type of dispatcher to be created.
        processor: The processor object to be used by the dispatcher.
    """

    dispatcher_type: str = field(default_factory=str)
    object_processer: Any = field(default_factory=lambda: "")

    def create_dispatcher(self) -> DispatcherTemplate:
        """
        Creates a dispatcher instance using the specified dispatcher type and object processor.

        Returns:
            DispatcherTemplate: An instance of a dispatcher.
        """

        dispatcher = DispatcherMapper()
        return dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher_type, obj=self.object_processer
        )

    def get_dispatcher(self) -> DispatcherTemplate:
        """
        Retrieves a dispatcher instance.

        Returns:
            DispatcherTemplate: An instance of a dispatcher.
        """

        return self.create_dispatcher()

    def get_value(self, key: str = "") -> Optional[Union[type, Path, None]]:
        """
        Retrieves a value from the dispatcher based on the provided key.

        Args:
            key (str, optional): The key for the value to be retrieved. Defaults to an empty string.

        Returns:
            Optional[Union[type, Path, None]]: The value associated with the key, or None if not found.
        """

        return self.get_dispatcher().get_value(key=key)
