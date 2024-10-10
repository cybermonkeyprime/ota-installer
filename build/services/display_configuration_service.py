from dataclasses import dataclass, field

import build.display as display


@dataclass
class DisplayConfigurationService(object):
    display_config: display.Configuration = field(default_factory=display.Configuration)

    def get_display_configuration(self) -> display.Configuration:
        return self.display_config
