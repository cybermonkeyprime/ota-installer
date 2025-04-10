from dataclasses import dataclass, field

from build.display import DisplayConfiguration


@dataclass
class DisplayDisplayConfigurationService(object):
    """
    Manages the configuration settings for a display.

    Attributes:
        configuration (DisplayConfiguration): The display configuration instance.
    """
    configuration: DisplayConfiguration = field(default_factory=DisplayConfiguration)

    def fetch_configuration(self) -> DisplayConfiguration:
        """Fetches the current display configuration.

        Returns:
            DisplayConfiguration: The current display configuration.
        """
        return self.configuration

def main() -> None:
    configuration_instance = DisplayConfiguration()

    display_manager = DisplayDisplayConfigurationService(configuration=configuration_instance)

    current_display_config = display_manager.fetch_configuration()
    print(current_display_config)

if __name__ == '__main__':
    main()
