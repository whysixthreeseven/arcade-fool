# Typing and annotations:
from typing import Any


def assert_value_type(check_value: Any, check_type: type | tuple[type, ...], raise_error: bool = True) -> bool:
    
    # Evaluating:
    assert_eval: bool = isinstance(check_value, check_type)
    
    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Invalid value type: <{type(check_value)}>. Expected <{check_type}>."
        raise AssertionError(error_message)
    
    # Returning:
    return assert_eval


def assert_value_default(check_value: Any, check_list: tuple[Any, ] | list[Any], raise_error: bool = True) -> bool:
    
    # Evaluating:
    assert_eval: bool = check_value in check_list

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears not to be default: <{check_value}>. Default list: <{check_list}>"
        raise AssertionError(error_message)
    
    
def assert_value_not_empty(check_value: str | list[Any] | tuple[Any, ...], raise_error: bool = True) -> bool:

    # Evaluating:
    if isinstance(check_value, str):
        assert_eval: bool = check_value != ""
    elif isinstance(check_value, (list, tuple)):
        assert_eval: bool = len(check_value) != 0

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears to be empty: <{check_value}>."
        raise AssertionError(error_message)

    # Returning:
    return assert_eval
    

def assert_value_ge_zero(check_value: int | float, raise_error: bool = True) -> bool:

    # Evaluating:
    assert_eval: bool = check_value >= 0

    # Raising error, if required:
    if not assert_eval and raise_error:
        error_message: str = f"Value appears to be negative: <{check_value}>."
        raise AssertionError(error_message)

    # Returning:
    return assert_eval

