from src.mobj_types.dynamic_or_uint import DynamicOrUint


def check_number_of_values_is_correct(
    value_count: DynamicOrUint, number_of_values: int
):
    if isinstance(value_count.value, int):
        if value_count.value != number_of_values:
            raise ValueError(
                f"Expected {value_count.value} values, got {number_of_values}"
            )
    else:
        if number_of_values == 0:
            raise ValueError(f"Expected at least 1 value, got {number_of_values}")


def check_no_defined_variable_is_used_as_a_variable(
    variable_list: list[set[str]], defined_variable_list: list[set[str]]
) -> None:
    """
    Check that no variable is used as a mobj defined variable and a mobj variable
    Example: (x < 2) => (forall x : x < 5) is invalid because in the expresion (x > 3) we don't know
    if x is a defined variable or not. So we can interpret it in 2 ways:
    - (x < 2) => (forall y : y < 5)
    - (x < 2) => (forall y : x < 5)
    """

    count = {}
    for variable_sublist in variable_list:
        for variable in variable_sublist:
            if variable in count:
                count[variable] += 1
            else:
                count[variable] = 1

    for defined_variable_sublist in defined_variable_list:
        for defined_variable in defined_variable_sublist:
            if count[defined_variable] > 1:
                raise ValueError(
                    f"Variable {defined_variable} is used as a defined variable and a variable"
                )


def check_no_variable_is_defined_twice(
    newly_defined_variables: set[str], already_defined_variables: set[str]
) -> None:
    """
    Check that no variable is used as a mobj defined variable two times, one inside another
    Example: forall x : (x < 3 => exists x : (x < 4)) is invalid because in the expresion (x < 4) we don't know what x is,
    as it can be interpreted in 2 ways:
    - forall x : (x < 3 => exists y : x < 4)
    - forall x : (x < 3 => exists y : (y < 4))
    """
    if set.intersection(newly_defined_variables, already_defined_variables) != set():
        raise ValueError(
            f"Variable {newly_defined_variables} is used as a mobj defined variable recursively"
        )
