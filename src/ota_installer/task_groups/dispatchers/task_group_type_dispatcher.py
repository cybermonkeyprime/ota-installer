# src/ota_installer/task_groups/dispatchers/task_group_type_dispatcher.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from ...log_setup import logger
from ..constants.task_group_names import TaskGroupNames

T = TypeVar("T")

K = TypeVar("K")
V = TypeVar("V", type, Path, str)
CollectionDictionary = dict[K, V]


@dataclass
class TaskGroupTypeDispatcher(object):
    obj: type = field(default_factory=lambda: type)
    data_enum: TaskGroupNames = field(init=False)
    collection: dict = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.collection = self.populate_collection()

        logger.debug(f"{self.collection=}")

    def populate_collection(self) -> dict:
        return {
            enum_member.name.lower(): enum_member._value(self.obj)
            for enum_member in TaskGroupNames
        }

    def get_instance(self, key: str) -> V | None:
        """
        Attempt to retrieve and instantiate the value associated with
            the given key.
        """

        try:
            task = self.collection.get(key)
            if not isinstance(task, Callable):
                raise ValueError(f"No task found for key: {key}")
            else:
                return task()
        except ValueError as err:
            logger.exception(f"{type(err).__name__} occurred at: {err}")
            return None
