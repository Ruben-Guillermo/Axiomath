# Unit tests for custom_mobj_values_verifier.py

import pytest
from src.mobj_types.dynamic_or_uint import DynamicOrUint
from src.mobjs.custom_mobj_values_verifier import (
    check_number_of_values_is_correct,
    check_no_defined_variable_is_used_as_a_variable,
    check_no_variable_is_defined_twice,
)


def test_number_of_values_is_correct():
    check_number_of_values_is_correct(DynamicOrUint(2), 2)
    check_number_of_values_is_correct(DynamicOrUint(0), 0)
    check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 1)
    check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 50)


def test_numbers_of_values_is_correct_invalid():
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint(2), 1)
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint(2), 3)
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 0)


def test_check_no_defined_variable_is_used_as_a_variable():
    check_no_defined_variable_is_used_as_a_variable([{"x", "y"}, {"z"}], [{"x"}, {"z"}])
    check_no_defined_variable_is_used_as_a_variable(
        [{"x", "y"}, {"z"}], [{"x", "y"}, {"z"}]
    )


def test_check_no_defined_variable_is_used_as_a_variable_invalid():
    with pytest.raises(ValueError):
        check_no_defined_variable_is_used_as_a_variable(
            [{"x", "y"}, {"z", "x"}], [{"x"}, {"x"}]
        )
    with pytest.raises(ValueError):
        check_no_defined_variable_is_used_as_a_variable(
            [{"x", "y"}, {"x", "y"}], [{"y"}, {"x"}]
        )
    with pytest.raises(ValueError):
        check_no_defined_variable_is_used_as_a_variable(
            [{"x", "y"}, {"z", "x"}], [{"x"}, {"x"}]
        )

def test_check_no_variable_is_defined_twice():
    check_no_variable_is_defined_twice({"x", "y"}, {"z"})
    check_no_variable_is_defined_twice({"x", "y"}, {"z"})
    

def test_check_no_variable_is_defined_twice_invalid():
    with pytest.raises(ValueError):
        check_no_variable_is_defined_twice({"x", "y"}, {"z", "x"})
    with pytest.raises(ValueError):
        check_no_variable_is_defined_twice({"x", "y"}, {"x", "y"})
