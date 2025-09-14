# Typing import:
from typing import Any


def assert_value_is_valid_type(check_value: Any, 
                               check_type: type | tuple[type, ...], 
                               raise_error: bool = True
                               ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Asserting value is within the expected type list:
    assert_eval: bool = isinstance(check_value, check_type)
    assert_error: str = f"Value {check_value=} is not expected type ({check_type=})."

    # Raising error (if enabled):
    if raise_error:
        assert assert_eval, assert_error

    # Returning (if reached):
    return assert_eval


def assert_value_is_default(check_value: Any,
                            check_list: tuple[Any, ...],
                            raise_error: bool = True
                            ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Asserting value is within the expected type list:
    assert_eval: bool = check_value in check_list
    assert_error: str = f"Value {check_value=} is not expected as default ({check_list=})."

    # Raising error (if enabled):
    if raise_error:
        assert assert_eval, assert_error

    # Returning (if reached):
    return assert_eval


def assert_value_in_valid_range(check_value: int | float,
                                check_range: range,
                                raise_error: bool = True
                                ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Asserting value is within the expected range:
    assert_eval: bool = int(check_value) in check_range
    assert_error: str = f"Value {check_value=} is not in expected range ({check_range=})."

    # Raising error (if enabled):
    if raise_error:
        assert assert_eval, assert_error

    # Returning (if reached):
    return assert_eval


def assert_value_is_positive(check_value: int | float,
                             raise_error: bool = True
                             ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Asserting value is positive:
    assert_eval: bool = check_value > 0
    assert_error: str = f"Value {check_value=} is negative, duh."

    # Raising error (if enabled):
    if raise_error:
        assert assert_eval, assert_error

    # Returning (if reached):
    return assert_eval
