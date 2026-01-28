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

