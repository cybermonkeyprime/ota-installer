# src/ota_installer/styles/containers/style_container.py
from typing import NamedTuple


class StyleContainer(NamedTuple):
    """Container for style attributes."""

    character: str
    spacing: int
    interval: int


# Signed off by Brian Sanford on 20260202
