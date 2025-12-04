from dataclasses import dataclass, field

import src.display.configurations as display_configs


@dataclass
class DisplayConfigurationService(object):
    display_conf: display_configs.Configuration = field(
        default_factory=display_configs.Configuration
    )

    def get_display_configuration(self) -> display_configs.Configuration:
        return self.display_conf
