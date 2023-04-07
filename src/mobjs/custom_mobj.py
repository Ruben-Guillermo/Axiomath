from src.mobjs.custom_mobj_values_verifier import (
    check_no_defined_variable_is_used_as_a_variable,
    check_no_variable_is_defined_twice,
    check_number_of_values_is_correct,
)
from src.mobjs.mobj import Mobj
from src.mobj_types.mobj_type import MobjType
from src.mobjs.variable import Variable


class CustomMobj(Mobj):
    """
    A custom mobj is a mobj that is not a primitive type
    It can contain other mobjs as values
    It is an instance of a mobj type
    """

    def __init__(self, type: MobjType, *values: Mobj) -> None:
        self._type = type
        self._values = values

        self._variables: set[str] = set()
        self._defined_variables: set[str] = set()

        newly_defined_variables = set()
        variable_list = []
        defined_variable_list = []

        structure = type.structure
        value_count = structure.value_count

        check_number_of_values_is_correct(value_count, len(values))

        for i, value in enumerate(values):
            # Check there are variables in the variable defining positions
            if structure.does_define and structure.is_spot_variable_defining(i):
                if not isinstance(value, Variable):
                    raise ValueError(
                        f"Expected a variable at index {i}, got {value} of type {value.type}"
                    )
                newly_defined_variables.add(value.var_name)

            variable_list.append(value.variables)
            defined_variable_list.append(value.defined_variables)

        check_no_defined_variable_is_used_as_a_variable(
            variable_list, defined_variable_list
        )

        self._variables = set.union(*variable_list) if len(variable_list) > 0 else set()
        self._defined_variables = (
            set.union(*defined_variable_list)
            if len(defined_variable_list) > 0
            else set()
        )

        check_no_variable_is_defined_twice(
            newly_defined_variables, self._defined_variables
        )
        self._defined_variables.update(newly_defined_variables)

    @property
    def type(self) -> MobjType:
        return self._type

    @property
    def variables(self) -> set[str]:
        return self._variables

    @property
    def defined_variables(self) -> set[str]:
        return self._defined_variables

    @property
    def values(self) -> tuple[Mobj]:
        return self._values

    def evaluate(self, values: dict[str, Mobj]) -> Mobj:
        evaluated_values = tuple(value.evaluate(values) for value in self._values)
        return CustomMobj(self._type, *evaluated_values)

    def create_dictionary_from(self, evaluation: Mobj) -> dict[str, Mobj]:
        if self.type != evaluation.type:
            raise ValueError(
                f"Cannot create dictionary from {self} and {evaluation} because they are of different types"
            )

        dictionary = {}

        for i, value in enumerate(self.values):
            new_dictionary = value.create_dictionary_from(evaluation.values[i])
            for key, value in new_dictionary.items():
                if not key in dictionary:
                    dictionary[key] = value
                else:
                    # check if the values are the same. If not, raise an error
                    # Example: (A => A), (A and B) => (A and C) -> raise error
                    if dictionary[key] != value:
                        raise ValueError(
                            f"Cannot create dictionary from {self} and {evaluation} because the values for key {key} are different"
                        )

        return dictionary

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, CustomMobj):
            return False

        return self.type == __value.type and self.values == __value.values
