# src/ota_installer/handler/task_group_handler.py
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from enum import Enum, StrEnum, auto

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..log_setup import logger
from ..plugin.plugin_registry import dispatcher_plugin
from ..task.task_info import TaskID

StrTuple = tuple[str, ...]
TaskGroupMap = Mapping["TaskGroupName", object]


@dataclass(frozen=True, slots=True)
class TaskGroupRenderer:
    task_class: type
    task_name: str

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Executes the task group's generation logic wrapped in the required UI
            decorators.
        """
        from .. import decorator

        # 1. This encapsulates your internal execution context
        def result():
            return self.task_class.get_member_names()

        # 2. Define the execution closure and apply your outer decorator
        @decorator.PaddedFooterWrapper()
        def execute_pipeline():
            # Apply your dynamic inner decorator
            decorated_function: Callable = decorator.ConfirmationPrompt(
                char=" ", comment=f"perform the {self.task_name}s"
            )(result)

            return decorated_function()

        # 3. Fire the pipeline and hand back the final tuple payload
        return execute_pipeline()


class TaskGroupName(StrEnum):
    """Enumeration for task group names."""

    PREPARATION = auto()
    MIGRATION = auto()
    APPLICATION = auto()

    def _get_value(self, _Class: type) -> object:
        """Retrieve the value from the given object based on the
        task group name.
        """
        return getattr(_Class, self.value)

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

    @classmethod
    def mapping(cls) -> Mapping[str, TaskGroupRenderer]:
        return {
            cls.PREPARATION: TaskGroupRenderer(
                PreparationTask, "Preparation Task"
            ),
            cls.MIGRATION: TaskGroupRenderer(MigrationTask, "Migration Task"),
            cls.APPLICATION: TaskGroupRenderer(
                ApplicationTask, "Application Task"
            ),
        }


@dataclass(frozen=True, slots=True)
class TaskGroupContainer:
    """Container for task group information."""

    group_name: str
    group_enum: TaskGroupName | None


class BehaviorBase(Enum):
    @property
    def task_name(self) -> str:
        """Return the lowercase name of the task."""
        return self.value.value

    @classmethod
    def get_member_names(cls) -> StrTuple:
        """Extracts task names from an enumeration."""
        return tuple(enum_member.value.value for enum_member in cls)


class ApplicationTask(BehaviorBase):
    """Enumeration of application tasks for OTA installation."""

    REBOOT_TO_RECOVERY = TaskID.REBOOT_TO_RECOVERY
    APPLY_OTA_UPDATE = TaskID.APPLY_OTA_UPDATE
    REBOOT_TO_BOOTLOADER = TaskID.REBOOT_TO_BOOTLOADER
    BOOT_TO_MAGISK_IMAGE = TaskID.BOOT_TO_MAGISK_IMAGE


class MigrationTask(BehaviorBase):
    """Enumeration of migration tasks with associated task IDs."""

    CHECK_ADB_CONNECTION = TaskID.CHECK_ADB_CONNECTION
    PUSH_STOCK_IMAGE = TaskID.PUSH_STOCK_IMAGE
    FIND_MAGISK_IMAGE = TaskID.FIND_MAGISK_IMAGE
    PULL_MAGISK_IMAGE = TaskID.PULL_MAGISK_IMAGE


class PreparationTask(BehaviorBase):
    """Enumeration of preparation tasks for OTA installation."""

    EXTRACT_PAYLOAD_IMAGE = TaskID.EXTRACT_PAYLOAD_IMAGE
    RENAME_PAYLOAD_IMAGE = TaskID.RENAME_PAYLOAD_IMAGE
    EXTRACT_STOCK_BOOT_IMAGE = TaskID.EXTRACT_STOCK_BOOT_IMAGE
    BACKUP_STOCK_BOOT_IMAGE = TaskID.BACKUP_STOCK_BOOT_IMAGE


@dispatcher_plugin(name=DispatcherType.TASK_GROUP.value)
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
        # Guard clause: If a dictionary mapping is passed directly, use it
        if isinstance(self.obj, dict):
            # Ensure keys are normalized to lowercase strings if that's what get_instance expects
            return {str(k).lower(): v for k, v in self.obj.items()}

        # Fall back to using the Enum introspection method if it's a class type
        if isinstance(self.obj, type):
            return TaskGroupName.create_dictionary(self.obj)

        logger.error(
            f"Unsupported object type passed to dispatcher: {type(self.obj)}"
        )
        return {}


# Signed off by Brian Sanford on 20260523
