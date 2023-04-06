from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.mobj_types.mobj_type import MobjType
    from src.mobjs.variable import Variable


class Mobj(ABC):
    @property
    @abstractmethod
    def type(self) -> MobjType:
        """Returns the type of the mobj"""

    @property
    @abstractmethod
    def variables(self) -> set[str]:
        """Returns the variables that are used in the mobj.
        Example: (x + y) -> {x, y}
        """

    @property
    @abstractmethod
    def defined_variables(self) -> set[str]:
        """Returns the variables that are defined in the mobj
        Example: (forall x: x > y) -> {x}
        """

    @property
    @abstractmethod
    def values(self) -> tuple[Mobj]:
        """Returns the values (childs mobj) that are used in the mobj.
        Example: (A and B) => (A or B) -> ((A and B), (A or B))
        """

    @abstractmethod
    def evaluate(self, values: dict[str, Mobj]) -> Mobj:
        """Evaluate the Mobj substituing some variables for other Mobjs
        Example: (A => B).evaluate({'A': (A and B), 'B': (A or B)}) -> (A and B) => (A or B)
        """

    @abstractmethod
    def create_dictionary_from(self, evaluation: Mobj) -> dict[str, Mobj]:
        """Create a dictionary from this mobj to another mobj,
        with variable names from self as keys and mobjs from evaluation as values.
        Example: (A => B),  (A and B) => (A or B) -> {'A': (A and B), 'B': (A or B)}
        """

    def get_sub_mobj(self, *indexes: int) -> Mobj:
        """Get a child mobj by index
        Example: (A and B) => (C or D).get_sub_mobj(0, 1) -> B
        """

        if len(indexes) == 0:
            return self

        index = indexes[0]
        if index >= len(self.values):
            raise IndexError(f"Index {index} out of range")

        return self.values[index].get_sub_mobj(*indexes[1:])
