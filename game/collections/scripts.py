# Annotations import:
from typing import Any

# Time library import:
from datetime import datetime


def clear_cached_property(target_object: object, target_attribute: str) -> None:
    """
    TODO: Create a docstring.
    """

    # Deleting attribute from an object if it exists:
    if hasattr(target_object, target_attribute):
        delattr(target_object, target_attribute)


def timestamp(self) -> str:
    """
    TODO: Create a docstring
    """

    # Generating a formatted timestamp string:
    time_now = datetime.now()
    time_pattern: str = "%H:%M:%S"
    time_formatted: str = datetime.strftime(
        time_now,
        time_pattern
        )
    
    # Returning:
    return time_formatted


def assert_value_is_valid_type(check_value: Any, 
                               valid_type: type, 
                               raise_error: bool = True
                               ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Evaluating:
    assert_eval: bool = isinstance(check_value, valid_type)
    assert_error: str = f"{check_value=} is not a valid type, expected: {valid_type=}."
    if raise_error:
        assert assert_eval, assert_error

    # Returning:
    return assert_eval


def assert_value_is_default(check_value: Any, 
                            valid_list: list[Any] | tuple[Any, ...], 
                            raise_error: bool = True
                            ) -> bool:
    """
    TODO: Create a docstring:
    """

    # Evaluating:
    assert_eval: bool = check_value in valid_list
    assert_error: str = f"{check_value=} is not an expected value, expected {valid_list=}."
    if raise_error:
        assert assert_eval, assert_error

    # Returning:
    return assert_eval


def assert_value_in_valid_range(check_value: int | float,
                                valid_range: range,
                                raise_error: bool = True
                                ) -> bool:
    """
    TODO: Create a docstring.
    """

    # Evaluating:
    assert_eval: bool = check_value in valid_range
    assert_error: str = f"{check_value=} is not in range {valid_range=}."
    if raise_error:
        assert assert_eval, assert_error

    # Returning:
    return assert_eval
