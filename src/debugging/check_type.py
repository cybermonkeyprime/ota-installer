from dataclasses import dataclass


@dataclass
class TypeChecker:
    name: str
    object_to_check: object

    def display_type_information(self) -> None:
        try:
            object_type: type = type(self.object_to_check)
            title = self.name.title()
            _object = self.object_to_check
            object_name = object_type.__name__
            print(f'{title}: "{_object}" is a {object_name}')
        except Exception as error:
            print(f"{self.name.title()}: {error}")

    def __str__(self) -> str:
        return str(self.display_type_information())


if __name__ == "__main__":
    print(TypeChecker(name="example", object_to_check=123))
