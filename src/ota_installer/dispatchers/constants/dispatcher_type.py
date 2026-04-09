# src/ota_installer/dispatchers/constants/dispatcher_type.py
from collections.abc import Callable
from enum import StrEnum, auto
from pathlib import Path

CollectionKeys = str
CollectionValues = Path | str
CollectionDictionary = dict[CollectionKeys, CollectionValues]


class DispatcherType(StrEnum):
    """Enumeration for dispatcher constants used in the OTA installer."""

    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()

    @classmethod
    def _dispatcher_mapping(cls):
        from ...directory.dispatchers.directory_dispatcher import (
            DirectoryDispatcher,
        )
        from ...images.boot_image.dispatchers.boot_image_dispatcher import (
            ImageTypeDispatcher,
        )
        from ...images.file_image.dispatchers.file_type_dispatcher import (
            FileTypeDispatcher,
        )
        from ...task_groups.dispatchers.task_group_type_dispatcher import (
            TaskGroupTypeDispatcher,
        )
        from ...variables.dispatchers.variable_type_dispatcher import (
            VariableTypeDispatcher,
        )

        return {
            cls.FILE.name: FileTypeDispatcher,
            cls.DIRECTORY.name: DirectoryDispatcher,
            cls.IMAGE.name: ImageTypeDispatcher,
            cls.TASK_GROUP.name: TaskGroupTypeDispatcher,
            cls.VARIABLE.name: VariableTypeDispatcher,
        }

    @classmethod
    def allowed_dispatchers(cls) -> tuple[str, ...]:
        """returns a tuple of allowed dispatcher names."""
        search = tuple(key for key in cls._dispatcher_mapping().keys())
        return search

    @classmethod
    def get_function(cls, key: str):
        return cls._dispatcher_mapping()[key.upper()]


# Final sign off by Brian Sanford on 20260317
