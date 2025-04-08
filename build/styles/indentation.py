from dataclasses import dataclass, field


@dataclass
class Indentation(object):
    """
    Represents an indentation level for text formatting.

    Attributes:
        interval (int): The indentation level.
        char (str): The character used for indentation.
        spacing (int): The number of spaces per indentation level.
    """
    interval: int # Rename to level
    char: str = field(default=" ") # Rename to character
    spacing: int = field(default=4) # Rename to spaces_per_level

    def __str__(self):
        """Returns the indentation as a string."""
        return f"{self.char[0] * self.spacing * self.interval}"

if __name__ == '__main__':
    # Example usage:
    basic_indent = Indentation(interval=1)
    print(f"Indented text:\n{basic_indent}This line is indented.")
