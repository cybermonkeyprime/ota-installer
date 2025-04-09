from dataclasses import dataclass, field

from build.display import Configuration


@dataclass
class DisplayConfigurationService(object): # Possibly rename to DisplayConfigurationManager
    """
    Manages the configuration settings for a display.

    Attributes:
        configuration (Configuration): The display configuration instance.
    """
    configuration: Configuration = field(default_factory=Configuration)

    def get_display_configuration(self) -> Configuration: # Rename to fetch_configuration
        """Fetches the current display configuration.

        Returns:
            Configuration: The current display configuration.
        """
        return self.configuration

def main() -> None:
    configuration_instance = Configuration()

    display_manager = DisplayConfigurationService(configuration=configuration_instance)

    current_display_config = display_manager.get_display_configuration()
    print(current_display_config)

if __name__ == '__main__':
    main()
