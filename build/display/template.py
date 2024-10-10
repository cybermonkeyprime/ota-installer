from typing import Protocol


class DisplayComponent(Protocol):
    def display(self) -> str:
        raise NotImplementedError()
