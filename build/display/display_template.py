from typing import Protocol


class DisplayComponent(Protocol):
    def get_display(self) -> str:
        raise NotImplementedError()
