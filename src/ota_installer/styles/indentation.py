# src/ota_installer/styles/indentation.py

from .containers.style_container import StyleContainer


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    """Creates an indentation string."""
    sc = StyleContainer(interval=interval, character=char[0], spacing=spaces)
    return f"{sc.character * sc.spacing * sc.interval}"


# Signed off by Brian Sanford on 20260119
