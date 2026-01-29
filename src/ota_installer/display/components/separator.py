# src/ota_installer/display/components/separator.py
from ...styles.separator import separator


def display_separator(indent=9, char="-") -> str:
    """Generates a formatted display separator."""
    formatted_separator = separator(indent, char[0])
    return f"{formatted_separator}> "


# Signed off by Brian Sanford on 20260129
