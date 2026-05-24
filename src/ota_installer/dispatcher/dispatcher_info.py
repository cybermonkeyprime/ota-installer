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
        from ..plugin.loader.dispatcher_plugin_loader import (
            DirectoryDispatcher,
            FileTypeDispatcher,
            ImageTypeDispatcher,
            TaskGroupTypeDispatcher,
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
        return tuple(cls._dispatcher_mapping())

    @classmethod
    def call_dispatcher(cls, key: str) -> type:
        """Retrieves the dispatcher class based on the key."""
        return cls._dispatcher_mapping()[key.upper()]

    @classmethod
    def check_dispatcher(cls, process_type: str) -> None:
        """Validates the dispatcher type."""
        if process_type.upper() not in cls.allowed_dispatchers():
            logger.error(
                f"Invalid dispatcher type: {process_type}."
                f"Allowed: {cls.allowed_dispatchers()}"
            )

    @classmethod
    def dispatcher_error(cls, process_type: str) -> None:
        if cls.call_dispatcher(key=process_type) is None:
            logger.error(f"Dispatcher mapping failed for: {process_type}")

    @classmethod
    def retrieve_dispatcher(cls, process_type, function_data) -> type | None:
        """Retrieves the dispatcher class based on the process type."""
        logger.debug(f"Retrieving dispatcher for process type: {process_type}")

        cls.check_dispatcher(process_type)
        cls.dispatcher_error(process_type)
        dispatcher_class: type = cls.call_dispatcher(key=process_type.upper())

        return dispatcher_class(function_data) if dispatcher_class else None

    def processor(
        self, processing_function: "VariableManager"
    ) -> "VariableItemProcessor":
        from ..display.variable.processor.variable_process_handler import (
            VariableItemProcessor,
        )

        return VariableItemProcessor(
            processing_function=processing_function,
            dispatcher_type=self.value,
        )


# Final sign off by Brian Sanford on 20260421
