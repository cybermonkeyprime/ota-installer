# task_group_handler.py
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto

from .dispatchers.constants.dispatcher_type import DispatcherType
from .dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from .dispatchers.templates.dispatcher_template import DispatcherTemplate
from .log_setup import logger
from .tasks.task_info import TaskID

StrTuple = tuple[str, ...]
TaskGroupMap = Mapping["TaskGroupName", object]


class TaskGroupName(StrEnum):
    """Enumeration for task group names."""

    PREPARATION = auto()
    MIGRATION = auto()
    APPLICATION = auto()

    def _get_value(self, obj: type) -> object:
        """Retrieve the value from the given object based on the
        task group name.
        """
        return getattr(obj, self.value)

    @classmethod
    def create_dictionary(cls, obj) -> TaskGroupMap:
        """create the dictionary with enum member names and their
        corresponding values.
        """
        return {
            enum_member: enum_member._get_value(obj) for enum_member in cls
        }

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()

    @classmethod
    def validation(cls, value: str) -> bool:
        """Validate the provided task group name."""
        return value.upper() in cls.__members__

    @classmethod
    def get_task_group_members(cls) -> StrTuple:
        """Returns the keys of the task groups."""
        return tuple(enum.value for enum in cls)


@dataclass(frozen=True, slots=True)
class TaskGroupContainer(object):
    """Container for task group information."""

    group_name: str
    group_enum: str | None


class BehaviorBase(Enum):
    @property
    def task_name(self) -> str:
        """Return the lowercase name of the task."""
        return self.value.value

    @classmethod
    def get_member_names(cls) -> tuple:
        """Extracts task names from an enumeration."""
        result: StrTuple = tuple(
            enum_member.value.value for enum_member in cls
        )
        logger.debug(f"enum_task_names(): {result=}")
        return result


class ApplicationTask(BehaviorBase):
    """Enumeration of application tasks for OTA installation."""

    REBOOT_TO_RECOVERY = TaskID.REBOOT_TO_RECOVERY
    APPLY_OTA_UPDATE = TaskID.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskID.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskID.BOOT_TO_MAGISK_IMAGE


class MigrationTask(BehaviorBase):
    """Enumeration of migration tasks with associated task IDs."""

    CHECK_ADB_CONNECTION = TaskID.CHECK_ADB_CONNECTION
    PUSH_STOCK_BOOT_IMAGE = TaskID.PUSH_STOCK_BOOT_IMAGE
    FIND_PATCHED_BOOT_IMAGE = TaskID.FIND_PATCHED_BOOT_IMAGE
    PULL_PATCHED_BOOT_IMAGE = TaskID.PULL_PATCHED_BOOT_IMAGE


class PreparationTask(BehaviorBase):
    """Enumeration of preparation tasks for OTA installation."""

    EXTRACT_PAYLOAD_IMAGE = TaskID.EXTRACT_PAYLOAD_IMAGE
    RENAME_PAYLOAD_IMAGE = TaskID.RENAME_PAYLOAD_IMAGE
    EXTRACT_STOCK_BOOT_IMAGE = TaskID.EXTRACT_STOCK_BOOT_IMAGE
    BACKUP_STOCK_BOOT_IMAGE = TaskID.BACKUP_STOCK_BOOT_IMAGE


@dispatcher_plugin(DispatcherType.TASK_GROUP.value)
@dataclass
class TaskGroupTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)
    data_enum: TaskGroupName = field(init=False)
    collection: TaskGroupMap = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.collection: TaskGroupMap = self.populate_collection()

        logger.debug(
            f"TaskGroupTypeDispatcher initialized with collection:"
            f"{self.collection}"
        )

    def populate_collection(self) -> TaskGroupMap:
        """Populate the collection with enum member names and their
        corresponding values.
        """
        return TaskGroupName.create_dictionary(self.obj)


# Signed off by Brian Sanford on 20260509
