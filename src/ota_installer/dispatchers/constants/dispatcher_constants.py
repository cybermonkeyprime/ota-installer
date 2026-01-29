# src/ota_installer/dispatchers/constants/dispatcher_constants.py
from enum import StrEnum, auto


class DispatcherConstants(StrEnum):
    """Enumeration for dispatcher constants used in the OTA installer."""

    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()


# Signed off by Brian Sanford on 20260129
