from collections.abc import Callable
from dataclasses import field
from pathlib import Path

CollectionValues = type | Path | None

CollectionDictionary = dict[str, CollectionValues]


class DispatcherTemplate:
    """A template class for dispatching tasks based on a key-value collection.

    Attributes:
        collection (dict[str, CollectionValues]): A dictionary mapping keys
        to their associated values or paths.
    """

    collection: CollectionDictionary = field(default_factory=dict)

    def get_value(self, key: str) -> CollectionValues:
        """Retrieve the value associated with the given key
        from the collection.

        Args:
            key (str): The key for which to retrieve the value.

        Returns:
            CollectionValues: The value associated with
            the key, or None if the key is not found.
        """

        return self.collection.get(key)

    def get_instance(self, key: str) -> Callable | None:
        """Attempt to retrieve and instantiate the value associated with
        the given key.

        Args:
            key (str): The key for which to retrieve and instantiate the value.

        Returns:
            Callable | None: The instantiated object if the value is callable
            and not None, otherwise None.

        Raises:
            ValueError: If no task is found for the given key.
        """

        try:
            task = self.get_value(key)
            if task is not None:
                return task()
            else:
                raise ValueError(f"No task found for key: {key}")
        except ValueError as err:
            print(err)
            return None
