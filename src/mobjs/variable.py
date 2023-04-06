from __future__ import annotations
from typing import Optional

from src.mobjs.mobj import Mobj
from src.validate_names import check_name_valid


class Variable(Mobj):
    """A representation of a mathematical variable. It is a Mobj that can be evaluated to a value.
    :param var_name: The name of the variable
    :type var_name: str

    """

    def __init__(self, var_name: str) -> None:
        check_name_valid(var_name)

        self._var_name = var_name

        self._variables = {self.var_name}
        self._defined_variables = set()

    @property
    def var_name(self):
        return self._var_name

    def __str__(self):
        return "[" + self.var_name + "]"

    def eval(self, value_dict: dict[str, Mobj]) -> Mobj:
        """Substitute the variable for its value if specified"""
        if self.var_name in value_dict:
            return value_dict[self.var_name]
        else:
            return Variable(self.var_name)

    def get_sub_mobj(self, *indexes: int) -> Mobj:
        if len(indexes) == 0:
            return self

        raise IndexError(
            f"Indexes are incorrect. Attempted to acces values {indexes} of variable {self.var_name}"
        )

    def substitute_sub_mobj(self, substitution: Mobj, *indexes: int) -> Mobj:
        if len(indexes) == 0:
            return substitution

        raise IndexError(
            f"Indexes are incorrect. Attempted to acces values {indexes} of variable {self.var_name}"
        )

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Variable):
            return False

        return self.var_name == __o.var_name

    def create_dictionary_from(
        self, evaluation: Mobj, var_dict: Optional[dict[str, Mobj]] = None
    ) -> dict[str, Mobj]:
        var_dict = var_dict if var_dict else {}

        if self.var_name in var_dict:
            # Check is correct
            if var_dict[self.var_name] != evaluation:
                raise ValueError(
                    f"Mobj provided {evaluation} is not a correct evaluation. Expected {var_dict[self.var_name]}"
                )

        else:
            var_dict[self.var_name] = evaluation

        return var_dict
