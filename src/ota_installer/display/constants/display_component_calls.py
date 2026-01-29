# src/ota_installer/display/constants/display_component_calls.py
from ..components.separator import display_separator
from ..components.subtitle import display_subtitle
from ..components.title import display_title
from .display_component import DisplayComponent

"""
This dict maps display components to their corresponding display functions.
"""
display_component_calls = {
    DisplayComponent.TITLE: display_title,
    DisplayComponent.SEPARATOR: display_separator,
    DisplayComponent.SUBTITLE: display_subtitle,
}


def call_display_component(component_type: DisplayComponent) -> str:
    """
    Call the display function associated with the given component type.
    """
    display_function = display_component_calls[component_type]
    if not display_function:
        raise ValueError(
            f"Display component {component_type} is not registered."
        )
    return display_function()
