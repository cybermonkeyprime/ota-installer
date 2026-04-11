# src/ota_installer/display/components/separator.py
from ...styles.separator import separator


def display_separator(indent: int = 9, char: str = "-") -> str:
    """Generates a formatted display separator."""
    formatted_separator = separator()
    return f"{formatted_separator}> "


# Signed off by Brian Sanford on 20260410
