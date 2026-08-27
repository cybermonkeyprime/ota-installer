# src/ota_installer/dispatcher/dispatcher_builder.py
from ..log_setup import logger
from .dispatcher_type import DispatcherType


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


def build_dispatcher_mapping() -> dict[DispatcherType, type]:
    from ..plugin.loader.dispatcher_plugin_loader import (
        DirectoryDispatcher,
        FileTypeDispatcher,
        ImageTypeDispatcher,
        TaskGroupTypeDispatcher,
        VariableTypeDispatcher,
    )

    return {
        DispatcherType.FILE: FileTypeDispatcher,
        DispatcherType.DIRECTORY: DirectoryDispatcher,
        DispatcherType.IMAGE: ImageTypeDispatcher,
        DispatcherType.TASK_GROUP: TaskGroupTypeDispatcher,
        DispatcherType.VARIABLE: VariableTypeDispatcher,
    }


# Signed off by Brian Sanford on 20260827
