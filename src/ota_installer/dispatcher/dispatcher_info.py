# src/ota_installer/dispatchers/constants/dispatcher_type.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from pathlib import Path
from typing import Protocol, cast, runtime_checkable

from ..log_setup import logger

type DispatcherFactory = Callable[[], object]
type CollectionValue = Path | str | DispatcherFactory
type CollectionDictionary = dict[Enum, CollectionValue]


class DispatcherType(StrEnum):
    """Enumeration for dispatcher constants used in the OTA installer."""

    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()

    @classmethod
    def allowed_dispatchers(cls):
        return tuple(member.value for member in cls)


@dataclass(frozen=True, slots=True)
class DispatcherDefinition:
    name: DispatcherType
    dispatcher_type: type

    def build(self, function_data: object) -> object:
        return self.dispatcher_type(function_data)


def build_dispatcher_mapping() -> dict[DispatcherType, type]:
    from ..plugin.loader.dispatcher_plugin_loader import (
        DirectoryHandler,
        FileTypeDispatcher,
        ImageTypeDispatcher,
        TaskGroupTypeDispatcher,
        VariableTypeDispatcher,
    )

    return {
        DispatcherType.FILE: FileTypeDispatcher,
        DispatcherType.DIRECTORY: DirectoryHandler,
        DispatcherType.IMAGE: ImageTypeDispatcher,
        DispatcherType.TASK_GROUP: TaskGroupTypeDispatcher,
        DispatcherType.VARIABLE: VariableTypeDispatcher,
    }


def build_dispatcher(
    process_type: str,
    function_data: object,
) -> object:
    normalized_type = process_type.strip().lower()
    allowed_dispatchers = DispatcherType.allowed_dispatchers()

    if normalized_type not in allowed_dispatchers:
        message = (
            f"Invalid dispatcher type: {process_type}. "
            f"Allowed: {allowed_dispatchers}"
        )
        logger.error(message)
        raise ValueError(message)

    dispatcher_name = DispatcherType(normalized_type)
    dispatcher_type = build_dispatcher_mapping()[dispatcher_name]

    return dispatcher_type(function_data)


@runtime_checkable
class DispatcherProtocol(Protocol):
    """Protocol defining the interface expected of all dispatchers."""

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
        """Normalize a key string for consistent internal usage."""
        ...


class DispatcherTemplate(DispatcherProtocol):
    """
    A template class for dispatching tasks based on a key-value collection.
    """

    collection: dict = {}

    def get_value(self, key: str) -> object | None:
        """Retrieve the value associated with the given key
        from the collection.
        """

        normalized_key = self.normalize_key(key)
        result = self.collection.get(self.normalize_key(key))

        if result is None:
            message = f"Key not found in collection: {normalized_key}"
            logger.error(message)
            raise KeyError(message)

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
            raise KeyError(message)

        if not callable(callback):
            message = (
                "Expected a callable object, "
                f"but got {type(callback).__name__}"
            )
            logger.error(message)
            raise TypeError(message)
        return cast(Callable, callback)()

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()


# Signed off by Brian Sanford on 20260714
