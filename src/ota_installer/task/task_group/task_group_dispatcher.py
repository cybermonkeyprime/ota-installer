# src/ota_installer/task/task_group_dispatcher.py
from dataclasses import dataclass, field
from functools import singledispatchmethod

from ...dispatcher.dispatcher_template import DispatcherTemplate
from ...dispatcher.dispatcher_type import DispatcherType
from ...log_setup import log_status
from ...plugin.plugin_registry import Plugin

TaskGroupMap = dict[str, object]


@Plugin.DISPATCHER.register(name=DispatcherType.TASK_GROUP.value)
@dataclass
class TaskGroupTypeDispatcher(DispatcherTemplate):
    obj: object = field(default_factory=lambda: dict)
    collection: TaskGroupMap = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.collection: TaskGroupMap = self.populate_collection()

        log_status(
            "debug",
            None,
            f"TaskGroupTypeDispatcher initialized with collection:"
            f"{self.collection}",
        )

    def populate_collection(self) -> TaskGroupMap:
        """Populate the collection with enum member names and their
        corresponding values.
        """
        return self.collection_type(self.obj)

    @singledispatchmethod
    def collection_type(self, obj) -> dict:
        log_status(
            "error",
            None,
            f"Unsupported object type passed to dispatcher: {type(obj)}",
        )
        return {}

    @collection_type.register
    def _(self, obj: dict) -> dict[str, object]:
        return {str(key).lower(): value for key, value in obj.items()}


# Signed off by Brian Sanford on 20260831
