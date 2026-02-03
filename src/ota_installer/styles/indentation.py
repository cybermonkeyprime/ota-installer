# src/ota_installer/styles/indentation.py

from .containers.style_container import StyleContainer


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    """Creates an indentation string."""
    style_container = StyleContainer(
        interval=interval, character=char[0], spacing=spaces
    )
    return (
        style_container.character
        * style_container.spacing
        * style_container.interval
    )


# Signed off by Brian Sanford on 20260203
