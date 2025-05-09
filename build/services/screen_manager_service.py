from dataclasses import dataclass, field

import logging
from build.display.display_screen_manager import ScreenManager


@dataclass
class ScreenManagerService(object):
    """
    A service class that provides an interface to manage screen operations.

    Attributes:
        screen_manager: An instance of ScreenManager to handle screen operations.
    """

    screen_manager: ScreenManager = field(default_factory=ScreenManager)

    def clear_screen(self) -> None:
        """Clears the screen using the screen manager."""
        try:
            self.screen_manager.clear_screen()
        except Exception as error:
            # Handle specific exceptions if needed
            logging.error(
                f"An error occurred while clearing the screen: {error}"
            )
            print(f"An error occurred while clearing the screen: {error}")
