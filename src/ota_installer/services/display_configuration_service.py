# src/ota_installer/services/display_configuration_service.py
from dataclasses import dataclass, field

from ..display.configurations import Configuration


@dataclass
class DisplayConfigurationService(object):
    display_conf: Configuration = field(default_factory=Configuration)

    def get_display_configuration(self) -> Configuration:
        return self.display_conf
