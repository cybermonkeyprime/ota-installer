# src/ota_installer/dispatcher/dispatcher_type.py
from enum import StrEnum, auto


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


# Signed off by Brian Sanford on 20260827
