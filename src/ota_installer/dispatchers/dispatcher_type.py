# src/ota_installer/dispatchers/constants/dispatcher_type.py
from enum import StrEnum, auto

from ..log_setup import logger


class DispatcherType(StrEnum):
    """Enumeration for dispatcher constants used in the OTA installer."""

    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()

    @classmethod
    def _dispatcher_mapping(cls) -> dict[str, type]:
        from ..directory_handler import (
            DirectoryDispatcher,
        )
        from ..images.boot_image_handler import (
            ImageTypeDispatcher,
        )
        from ..images.generic_image_handler import (
            FileTypeDispatcher,
        )
        from ..task_group_handler import (
            TaskGroupTypeDispatcher,
        )
        from ..variables.variable_handler import (
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
        """Returns a tuple of allowed dispatcher names."""
        return tuple(key for key in cls._dispatcher_mapping().keys())

    @classmethod
    def call_dispatcher(cls, key: str) -> type:
        """Retrieves the dispatcher class based on the key."""
        return cls._dispatcher_mapping()[key.upper()]

    @classmethod
    def check_dispatcher(cls, process_type) -> None:
        """Validates the dispatcher type."""
        allowed_dispatchers = cls.allowed_dispatchers()
        if process_type.upper() not in allowed_dispatchers:
            logger.error(
                f"Invalid dispatcher type: {process_type}."
                f"Allowed: {allowed_dispatchers}"
            )
            return None

    @classmethod
    def dispatcher_error(cls, process_type):
        if cls.call_dispatcher(process_type) is None:
            logger.error(f"Dispatcher mapping failed for: {process_type}")
            return None

    @classmethod
    def retrieve_dispatcher(cls, process_type, function_data) -> type | None:
        """Retrieves the dispatcher class based on the process type."""
        logger.debug(f"Retrieving dispatcher for process type: {process_type}")

        cls.check_dispatcher(process_type)
        cls.dispatcher_error(process_type)
        dispatcher_name = cls.call_dispatcher(process_type.upper())

        return dispatcher_name(function_data)


# Final sign off by Brian Sanford on 20260421
