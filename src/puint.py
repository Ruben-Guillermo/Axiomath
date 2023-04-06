from enum import Enum, auto
from typing import Union


class UndefinedEnum(Enum):
    UNDEFINED = auto()


class PositiveOrUndefinedInt:
    """A class that represents a positive integer or undefined. x > 0 or undefined"""

    def __init__(self, value: Union[int, UndefinedEnum]):
        self.value = value
        if isinstance(value, int):
            if value <= 0:
                raise ValueError(
                    f"Value must be positive or undefined. Provided {value}"
                )
        elif value != UndefinedEnum.UNDEFINED:
            raise ValueError(f"Value must be positive or undefined. Provided {value}")

    def __eq__(self, other):
        if not isinstance(other, PositiveOrUndefinedInt):
            return False

        return self.value == other.value

    @property
    def defined(self) -> bool:
        return isinstance(self.value, int)
