from dataclasses import dataclass, field


@dataclass
class ErrorMessage(object):
    """Represents an error that occurred during item processing."""

    item_title: str = field(default="")
    item_name: str = field(default="")
    error_message: Exception = field(default_factory=Exception)

    def __str__(self) -> str:
        return (
            f"Error processing {self.item_title} {self.item_name}: {self.error_message}"
        )
