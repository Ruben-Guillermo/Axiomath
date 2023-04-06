from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class Mobj(ABC):
    """A representation of a mathematical object, such as a set or a proposition.
    Variables, types of propositions (implication, conjunction) and types of sets (union, cartesian product) are all examples of Mobjs.

    :param variables: All variables that appear in the Mobj, like A in 'A implies B'
    :type variables: set[str]
    :param defined_variables: All variables that are defined in the Mobj, like x in '{x | x is a natural number}'
    :type defined_variables: set[str]
    """

    _variables: set[str]
    _defined_variables: set[str]

    @property
    def variables(self) -> set[str]:
        """All variables that appear in the Mobj, like A in 'A implies B'"""
        return self._variables

    @property
    def defined_variables(self) -> set[str]:
        """All variables that are defined in the Mobj, like x in '{x | x is a natural number}'"""
        return self._defined_variables

    def __repr__(self) -> str:
        return str(self)

    @abstractmethod
    def __str__(self) -> str:
        """Create a string representation of the Mobj"""

    @abstractmethod
    def eval(self, value_dict: dict[str, Mobj]) -> Mobj:
        """Evaluate the Mobj substituing some variables for other Mobjs"""

    @abstractmethod
    def get_sub_mobj(self, *indexes: int) -> Mobj:
        """Get a child mobj of the values of self"""

    @abstractmethod
    def substitute_sub_mobj(self, substitution: Mobj, *indexes: int) -> Mobj:
        """Get a new mobj that substitutes its value at the given indexes for a substitution"""

    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass

    @abstractmethod
    def create_dictionary_from(
        self, evaluation: Mobj, var_dict: Optional[dict[str, Mobj]] = None
    ) -> dict[str, Mobj]:
        """Create a dictionary from self and an evaluation of it whith variable names as keys.
        If a dictionary is provided, it will be updated with the values"""
