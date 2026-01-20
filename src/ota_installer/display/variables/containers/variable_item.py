# src/ota_installer/display/variables/classes/variable_item.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class VariableItem(object):
    """Represents a variable item with a title and a value."""

    title: str
    value: str | None


# Signed off by Brian Sanford on 20260119
