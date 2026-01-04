# src/ota_installer/display/configurations/display_configuration.py

from ...log_setup import logger
from ..display_all_components import show_display_components


def create_version_display() -> None:
    try:
        show_display_components()
    except AttributeError as err:
        logger.error(f"AttributeError: {err}")
    except Exception as error:
        logger.exception(f"Failed to create version display: {error}")


if __name__ == "__main__":
    pass
