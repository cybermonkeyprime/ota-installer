# src/ota_installer/styles/indentation.py

from collections import namedtuple

IndentationContainer = namedtuple(
    "IndentationContainer", ["character", "spacing", "interval"]
)


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    ic = IndentationContainer(
        interval=interval, character=char[0], spacing=spaces
    )
    return f"{ic.character * ic.spacing * ic.interval}"
