# src/ota_installer/dispatchers/constants/dispatcher_type.py
from collections.abc import Callable, Mapping
from enum import StrEnum, auto
from pathlib import Path
from typing import Protocol, runtime_checkable

from ..log_setup import logger

CollectionKeys = str
CollectionValues = Path | str
CollectionDictionary = Mapping[CollectionKeys, CollectionValues]


class DispatcherType(StrEnum):
    """Enumeration for dispatcher constants used in the OTA installer."""

    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()

    @classmethod
    def fetch_mapping(cls) -> dict[str, type]:
        from ..plugin.loader.dispatcher_plugin_loader import (
            DirectoryHandler,
            FileTypeDispatcher,
            ImageTypeDispatcher,
            TaskGroupTypeDispatcher,
            VariableTypeDispatcher,
        )

        return {
            cls.FILE.name: FileTypeDispatcher,
            cls.DIRECTORY.name: DirectoryHandler,
            cls.IMAGE.name: ImageTypeDispatcher,
            cls.TASK_GROUP.name: TaskGroupTypeDispatcher,
            cls.VARIABLE.name: VariableTypeDispatcher,
        }

    @classmethod
    def allowed_dispatchers(cls) -> tuple[str, ...]:
        """Returns a tuple of allowed dispatcher names."""
        return tuple(cls.fetch_mapping())

    @classmethod
    def call_dispatcher(cls, key: str) -> type:
        """Retrieves the dispatcher class based on the key."""
        return cls.fetch_mapping()[key.upper()]

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

    @classmethod
    def get_dispatcher(cls, process_type, function_data) -> type | None:
        """Retrieves the dispatcher for the given process type."""
        logger.debug("DispatcherType.get_dispatcher(): function_data")
        return cls.retrieve_dispatcher(process_type, function_data)


@runtime_checkable
class DispatcherProtocol(Protocol):
    """
    Protocol defining the interface expected of all dispatchers.
    Ensures compatibility across dispatcher variants and promotes consistent
    behavior.
    """

    collection: dict[str, object]

    def get_value(self, key: str) -> object:
        """
        Retrieve a value from the internal collection using the provided key.
        """
        ...

    def get_instance(self, key: str) -> object | None:
        """Retrieve an instance from the collection using the provided key."""
        ...

    @staticmethod
    def normalize_key(key: str) -> str:
        """
        Normalize a key string for consistent internal usage.
        Typical implementations may use lowercasing, stripping, or other
        formatting.
        """
        ...


class DispatcherTemplate(DispatcherProtocol):
    """
    A template class for dispatching tasks based on a key-value collection.
    """

    collection: CollectionDictionary = {}

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """

        result = self.collection.get(self.normalize_key(key))

        if not result:
            logger.exception(f"Value is {key} not found")

        return result

    def get_instance(self, key: str) -> Callable:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        normalized_key = self.normalize_key(key)
        callback = self.collection.get(normalized_key)

        if callback is None:
            message = f"Key not found in collection: {normalized_key}"
            logger.critical(message)
            raise ValueError(message)

        if not callable(callback):
            message = (
                "Expected a callable object, "
                f"but got {type(callback).__name__}"
            )
            logger.error(message)
            raise TypeError(message)
        return callback()

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()


