# src/ota_installer/task_groups/dispatchers/task_group_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import TypeVar

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ...dispatchers.templates.dispatcher_template import DispatcherTemplate
from ...log_setup import logger
from ..constants.task_group_names import TaskGroupNames

T = TypeVar("T")

K = TypeVar("K")
V = TypeVar("V", type, Path, str)
CollectionDictionary = dict[K, V]


@dispatcher_plugin(DispatcherConstants.TASK_GROUP.value)
@dataclass
class TaskGroupTypeDispatcher(DispatcherTemplate):
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
