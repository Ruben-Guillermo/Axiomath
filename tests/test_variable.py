# Unit tests for the variable module

from src.mobjs.variable import Variable


def test_variable_default():
    var = Variable("x")
    assert var.var_name == "x"
    assert var.variables == {"x"}
    assert var.defined_variables == set()


def test_variable_eval():
    var = Variable("x")
    assert var.eval({}) == var
    assert var.eval({"x": Variable("y")}) == Variable("y")


def test_eq():
    var = Variable("x")
    assert var == Variable("x")
    assert var != Variable("y")
    assert var != 1


def test_str():
    var = Variable("x")
    assert str(var) == "[x]"


def test_make_dictionary():
    var = Variable("x")

    # basic creation
    assert var.create_dictionary_from(Variable("y")) == {"x": Variable("y")}
    # if the variable is already in the dictionary, assert that the value is correct
    assert var.create_dictionary_from(Variable("y"), {"x": Variable("y")}) == {
        "x": Variable("y")
    }


def test_make_dictionary_error():
    var = Variable("x")

    # if the variable is already in the dictionary, assert that the value is correct
    try:
        var.create_dictionary_from(Variable("z"), {"x": Variable("y")})
    except ValueError:
        pass
    else:
        raise AssertionError("Expected a ValueError to be raised")


def test_get_sub_mobj():
    var = Variable("x")

    assert var.get_sub_mobj() == var
    try:
        var.get_sub_mobj(1)
    except IndexError:
        pass
    else:
        raise AssertionError("Expected an IndexError to be raised")


def test_substitute_sub_mobj():
    var = Variable("x")

    assert var.substitute_sub_mobj(Variable("y")) == Variable("y")
    try:
        var.substitute_sub_mobj(Variable("y"), 1)
    except IndexError:
        pass
    else:
        raise AssertionError("Expected an IndexError to be raised")
