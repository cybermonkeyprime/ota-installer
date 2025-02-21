from collections.abc import Callable
from typing import Union


class DispatcherTemplate:
    collection: dict[str, type] = {}

    def get_value(self, key: str) -> Union[type, None]:
        return self.collection.get(key)

    def get_instance(self, key: str) -> Callable | None:
        try:
            task = self.get_value(key)
            if task is not None:
                return task()
            else:
                raise ValueError(f"No task found for key: {key}")
        except ValueError as err:
            print(err)
            return None
