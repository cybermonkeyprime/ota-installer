from dataclasses import dataclass, field

from src.display.managers import ScreenManager


@dataclass
class ScreenManagerService(object):
    screen_manager: ScreenManager = field(default_factory=ScreenManager)

    def clear_screen(self) -> None:
        self.screen_manager.clear_screen()
