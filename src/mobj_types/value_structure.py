from __future__ import annotations

from typing import Optional
from src.mobj_types.dynamic_or_uint import Dynamic, DynamicOrUint


class ValueStructure:
    """Represent a structure for the values of the mobj, with the following restriction:
    - If the value_count is dynamic, then there cannot be any variable defining spots
    """

    def __init__(
        self, value_count: DynamicOrUint, variable_defining_spots: Optional[list[bool]]
    ):
        self.value_count = value_count

        if value_count.is_int:
            if (
                variable_defining_spots == None
                or not len(variable_defining_spots) == value_count.value
            ):
                raise ValueError(
                    f"""
                    If value_count is an int, then defined_variable_spots must be a list of that length.
                    Got value_count: {value_count.value}, defined_variable_spots: {variable_defining_spots}
                    """
                )

            self.variable_defining_spots = variable_defining_spots
            self.does_define = any(variable_defining_spots)

        else:
            if variable_defining_spots:
                raise ValueError(
                    "If value_count is dynamic, then defined_variable_spots must be None"
                )
            self.variable_defining_spots = []
            self.does_define = False

    def is_spot_variable_defining(self, spot: int) -> bool:
        return self.variable_defining_spots[spot] if self.does_define else False

    def __eq__(self, other: ValueStructure) -> bool:
        return (
            self.value_count == other.value_count
            and self.variable_defining_spots == other.variable_defining_spots
        )

    @staticmethod
    def dynamic() -> ValueStructure:
        return ValueStructure(DynamicOrUint(Dynamic.GREATER_THAN_0), None)

    @staticmethod
    def non_defining(value_count: int) -> ValueStructure:
        return ValueStructure(DynamicOrUint(value_count), [False] * value_count)

    @staticmethod
    def defines_first(value_count: int) -> ValueStructure:
        return ValueStructure(
            DynamicOrUint(value_count), [True] + [False] * (value_count - 1)
        )
