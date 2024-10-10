from dataclasses import dataclass
from typing import Any, Type


@dataclass
class TypeChecker:
    name: str
    object_to_check: Any

    def display_type_information(self) -> None:
        try:
            object_type: Type = type(self.object_to_check)
            print(
                f'{self.name.title()}: "{self.object_to_check}" is a {object_type.__name__}'
            )
        except Exception as error:
            print(f"{self.name.title()}: {error}")

    def __str__(self) -> str:
        return str(self.display_type_information())


if __name__ == "__main__":
    print(TypeChecker(name="example", object_to_check=123))
