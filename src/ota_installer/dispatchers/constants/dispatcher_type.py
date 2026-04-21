# src/ota_installer/dispatchers/constants/dispatcher_type.py
from enum import StrEnum, auto
from pathlib import Path

from ...log_setup import logger

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
        from ...images.boot_image.constants.boot_image_type import (
            BootImageType,
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
            cls.IMAGE.name: BootImageType,
            cls.TASK_GROUP.name: TaskGroupTypeDispatcher,
            cls.VARIABLE.name: VariableTypeDispatcher,
        }

    @classmethod
    def allowed_dispatchers(cls) -> tuple[str, ...]:
        """returns a tuple of allowed dispatcher names."""
        search = tuple(key for key in cls._dispatcher_mapping().keys())
        return search

    @classmethod
    def get_function(cls, key: str) -> type:
        return cls._dispatcher_mapping()[key.upper()]

    @classmethod
    def dispatcher_check(cls, process_type) -> None:
        allowed_dispatchers = cls.allowed_dispatchers()
        if process_type.upper() not in allowed_dispatchers:
            logger.error(
                f"Invalid dispatcher type: {process_type}."
                f"Allowed: {allowed_dispatchers}"
            )
            return None

    @classmethod
    def dispatcher_error(cls, process_type):
        if cls.get_function(process_type) is None:
            logger.error(f"Dispatcher mapping failed for: {process_type}")
            return None

    @classmethod
    def retrieve_dispatcher(cls, process_type, function_call) -> type | None:
        """Retrieves the dispatcher class based on the process type."""
        logger.debug(f"Retrieving dispatcher for process type: {process_type}")

        cls.dispatcher_check(process_type)

        dispatcher_name = cls.get_function(process_type.upper())

        cls.dispatcher_error(process_type)

        return dispatcher_name(function_call)


# Final sign off by Brian Sanford on 20260317
