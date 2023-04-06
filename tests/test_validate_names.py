# unit tests for the validate_names module

from src.validate_names import check_name_valid, check_replacement_string_valid, NamingError
import pytest

def test_check_name_valid_default():
    assert check_name_valid("x") == None
    assert check_name_valid("x y") == None
    assert check_name_valid("xyz") == None
    assert check_name_valid("x y z") == None
    assert check_name_valid("x1") == None
    assert check_name_valid("x1+y2") == None
    assert check_name_valid("x1 +.-y2<") == None
    
def test_check_name_valid_error():
    with pytest.raises(NamingError):
        check_name_valid("")
    with pytest.raises(NamingError):
        check_name_valid("x$")
    with pytest.raises(NamingError):
        check_name_valid("x$13")
    with pytest.raises(NamingError):
        check_name_valid("$1")
        
def test_check_replacement_string_valid_default():
    assert check_replacement_string_valid("x") == None
    assert check_replacement_string_valid("x y") == None
    assert check_replacement_string_valid("xyz") == None
    assert check_replacement_string_valid("x y z") == None
    assert check_replacement_string_valid("$1") == None
    assert check_replacement_string_valid("x$1") == None
    assert check_replacement_string_valid("x$1y$2") == None
    assert check_replacement_string_valid("$1$2") == None
    assert check_replacement_string_valid("$1 $2") == None
    assert check_replacement_string_valid("$1 + $2") == None
    
    
    
def test_check_replacement_string_valid_error():
    with pytest.raises(NamingError):
        check_replacement_string_valid("")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$$")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$x")
    with pytest.raises(NamingError):
        check_replacement_string_valid("x$")
    with pytest.raises(NamingError):
        check_replacement_string_valid("x$$")
    with pytest.raises(NamingError):
        check_replacement_string_valid("1")
    with pytest.raises(NamingError):
        check_replacement_string_valid("1$1")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$1$")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$1 $")
    with pytest.raises(NamingError):
        check_replacement_string_valid("$1 2")

