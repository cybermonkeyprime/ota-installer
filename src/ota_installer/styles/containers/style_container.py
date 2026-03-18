# src/ota_installer/styles/containers/style_container.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StyleContainer(object):
    """Container for style attributes."""

    character: str
    spacing: int
    interval: int


# Signed off by Brian Sanford on 20260318
