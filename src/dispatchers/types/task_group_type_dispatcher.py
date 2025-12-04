# src/dispatchers/types/task_group_type_dispatcher.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

import src.dispatchers.mappings as dispatcher_mappings
from src.logger import logger

T = TypeVar("T")

CollectionKeys = TypeVar("CollectionKeys")
CollectionValues = TypeVar("CollectionValues", type, Path, str)
CollectionDictionary = dict[CollectionKeys, CollectionValues]


@dataclass
class TaskGroupTypeDispatcher(object):
    obj: type = field(default_factory=lambda: type)
    data_enum: dispatcher_mappings.TaskGroupTypeMapping = field(init=False)
    collection = {}

    def __post_init__(self) -> None:
        for enum in dispatcher_mappings.TaskGroupTypeMapping:
            self.collection[enum.name.lower()] = enum._value(self.obj)

    def get_instance(self, key: str) -> CollectionValues | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        try:
            task = self.collection.get(key)
            if isinstance(task, Callable):
                return task()
            else:
                raise ValueError(f"No task found for key: {key}")
        except ValueError as err:
            logger.exception(f"{type(err).__name__} occurred at: {err}")
            return None
