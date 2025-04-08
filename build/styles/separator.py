from dataclasses import dataclass, field
from build.styles.indentation import Indentation


@dataclass
class Separator(object): # Rename LineSeparator
    """Represents a line separator with a customizable character and increment.

    Attributes:
        increment (int): The number of times the character is repeated.
        character (str): The character used for the line separator.
    """
    increment: int = field(default=1)
    char: str = field(default="-") # Rename character

    def __str__(self) -> str:
        return f"{Indentation(char=self.char[0], interval=self.increment)}"
        # return f"{self.char * 4 * self.increment}"

if __name__ == '__main__':
    # Example usage:
    default_separator = Separator()
    custom_separator = Separator(increment=2, char="*")
    print(str(default_separator))  # Output: ----
    print(str(custom_separator))  # Output: ********
